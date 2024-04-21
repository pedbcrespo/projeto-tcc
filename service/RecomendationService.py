from model.City import City
from model.State import State
from model.InfoLightConsume import InfoLightConsume
from model.InfoLightPrice import InfoLightPrice
from model.InfoWaterConsumer import InfoWaterConsumer
from model.InfoWaterPriceRegion import InfoWaterPriceRegion
from model.InfoInternet import InfoInternet
from model.InfoCoustLiving import InfoCoustLiving
from model.Questions import AttributesPoints
from model.FormResult import FormResult
from service.InfoService import InfoService
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft
from typing import List

class RecomendationService:
    infoService = InfoService()
    def getRecomendation(self, formResult):
        listformResultObj = list(map(lambda res: FormResult(res), formResult))
        attributePoints = self.__calculateAttributes__(listformResultObj)
        sortedListAttributes = sorted(attributePoints.getOrdenationAttributeList(), key=lambda att: att['value'], reverse=True)
        listAttributeKeys = list(map(lambda att: att['key'], sortedListAttributes))
        attributesHandleRelated = {
            'LIVING_QUALITY': self.__getBetterIdh__,
            'EMPLOYABILITY': self.__getBetterBusinessSAccessibility__,
            'LEISURE': self.__getBetterEntertainment__,
            'COST': self.__getBetterCoust__,
        }
        attributesKey = {
            'LIVING_QUALITY': 'idh',
            'EMPLOYABILITY': 'business_accessibility',
            'LEISURE' : 'recreation_rate',
            'COST': 'total'
        }
        cities = self.__getCitiesToRecomendation__(attributePoints)
        print('================================')
        print(listAttributeKeys)
        for att in listAttributeKeys:
            print('================================')
            print('analisando:', att)
            cities = attributesHandleRelated[att](cities)
        print('================================')

        def handleSortedCity(city):
            listAtt = [city.infoValue[attributesKey[att]] for att in listAttributeKeys]
            return tuple(listAtt)
        
        sortedCities = sorted(cities, key=lambda city: handleSortedCity(city))
        return self.__handleInfo__(sortedCities)

    def __handleInfo__(self, sortedCities):
        infos = []
        for city in sortedCities:
            dictCity = city.json()
            dictCity.update(self.infoService.getCityInfo(city.id))
            dictCity.update(self.infoService.getDetailsInfo(city.id))
            infos.append(dictCity)
        return infos

    def __createSession__(self):
        engine = create_engine(conn)
        Session = sessionmaker(bind=engine)
        return Session()

    def __calculateAttributes__(self, listFormResult: List[FormResult]) -> AttributesPoints:
        generalPontuation = {}
        ordenationAttributes = {}
        for formatResult in listFormResult: 
            for key in formatResult.increase:
                if key not in ordenationAttributes:
                    ordenationAttributes[key] = 0
                ordenationAttributes[key] += formatResult.answer
        
            for key in formatResult.decrease:
                if key not in ordenationAttributes:
                    ordenationAttributes[key] = 0
                ordenationAttributes[key] -= formatResult.answer
                if ordenationAttributes[key] < 0:
                    ordenationAttributes[key] = 0

            resultJson = formatResult.json()
            for key in formatResult.pontuations:
                if key not in generalPontuation:
                    generalPontuation[key] = {'total': 0, 'count': 0}
                generalPontuation[key]['total'] += resultJson['pontuations'][key]
                generalPontuation[key]['count'] += 1
        
        for key in generalPontuation:
            total = generalPontuation[key]['total']
            count = generalPontuation[key]['count']
            generalPontuation[key]['avg'] = round(total/count, 2)

        return AttributesPoints(ordenationAttributes, generalPontuation)
    
    def __getBetter__(self, cities, methodsComparation, keyComparation, qtd, reverse=True):
        if cities == None:
            cities = City.query.all()
        for city in cities:
            if not hasattr(city, 'infoValue'):
                city.infoValue = {}
            city.infoValue.update(methodsComparation(city.id))
        cities = sorted(cities, key=lambda city: city.infoValue[keyComparation], reverse=reverse)
        return cities if len(cities) == qtd else cities[:qtd]

    def __getBetterIdh__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.infoService.getIdh, 'idh', qtd)
    
    def __getBetterBusinessSAccessibility__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.infoService.getProfissionalQualificationRate, 'business_accessibility', qtd)
    
    def __getBetterEntertainment__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.infoService.getEntertainmentRate, 'recreation_rate', qtd)
    
    def __getBetterCoust__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.infoService.__getTotalCoust__, 'total', qtd, False)
    
    def __getCitiesToRecomendation__(self, attributesPoints: AttributesPoints) -> List[City]:
        print('total attributes', attributesPoints.getTotal())
        allCities = City.query.all()
        cities = allCities
        citiesFiltered = self.__filteredCitiesByWaterAndLightConsume__(cities, attributesPoints)
        avgWaterConsume = attributesPoints.subAttributes['ltWaterConsume']
        avgLightConsume = attributesPoints.subAttributes['hoursLightEstiamte']
        with self.__createSession__() as session:
            query = session.query(
                City.id.label('city_id'),
                State.id.label('state_id'),
                (
                    func.round(InfoWaterPriceRegion.price * avgWaterConsume, 2) +
                    func.round(InfoLightPrice.price_kwh * avgLightConsume, 2) +
                    (InfoCoustLiving.alimentation + InfoCoustLiving.transport + InfoCoustLiving.health + InfoCoustLiving.hygiene + InfoCoustLiving.recreation + InfoInternet.avg_price)
                ).label('can_living')
            ).join(State, State.id == City.state_id
            ).join(InfoWaterPriceRegion, State.region_id == InfoWaterPriceRegion.region_id
            ).join(InfoWaterConsumer, InfoWaterConsumer.state_id == State.id
            ).join(InfoLightPrice, InfoLightPrice.state_id == State.id
            ).join(InfoLightConsume, InfoLightConsume.state_id == State.id
            ).join(InfoCoustLiving, InfoCoustLiving.state_id == State.id
            ).join(InfoInternet, InfoInternet.city_id == City.id)
            results = query.all()

            def filterByStateTotal(result, attributesPoints):
                totalCoustPrice = result[2]
                state = State.query.filter(State.id == result[1]).first()
                return totalCoustPrice <= attributesPoints.getTotal(state)

            filteredResults = list(filter(lambda result: filterByStateTotal(result, attributesPoints), results))
            filteredResultsCityIds = list(map(lambda result: result[0], filteredResults))
            cities = list(filter(lambda city: city.id in filteredResultsCityIds, citiesFiltered))
        return cities if len(cities) >= 0 else allCities
    
    def __filteredCitiesByWaterAndLightConsume__(self, cities: List[City], attributesPoints: AttributesPoints) -> List[City]:
        avgLightConsume = attributesPoints.subAttributes['hoursLightEstiamte']
        avgWaterConsume = attributesPoints.subAttributes['ltWaterConsume']
        filteredCities = []
        with self.__createSession__() as session:
            query = session.query(
                State.id.label('state_id'),
                InfoWaterConsumer.amount.label('water_consume'),
                func.round((InfoLightConsume.amount / 12), 2).label('light_consume'),
            ).join(InfoWaterConsumer, InfoWaterConsumer.state_id == State.id
            ).join(InfoLightConsume, InfoLightConsume.state_id == State.id)
            results = query.all()
            statesFilteredByConsume = list(filter(lambda res: res[1] <= avgWaterConsume * 1.1 and res[2] <= avgLightConsume * 1.1, results))
            stateIds = list(map(lambda filteredResult: filteredResult[0], statesFilteredByConsume))
            filteredCities = list(filter(lambda city: city.state_id in stateIds, cities))

        states = State.query.filter(State.id in list(map(lambda city: city.state_id, filteredCities))).all()
        lightPrices = InfoLightPrice.query.filter(InfoLightPrice.state_id in list(map(lambda st: st.id, states)))
        waterPrices = InfoWaterPriceRegion.query.filter(InfoWaterPriceRegion.region_id in list(map(lambda st: st.region_id, states)))

        # AQUI CALCULO O PRECO DA LUZ E DA AGUA POR ESTADO
        attributesPoints.pricesLight = [{'state_id': lightPrice.state_id,'value': avgLightConsume * lightPrice.price_kwh} for lightPrice in lightPrices]
        attributesPoints.pricesWater = [{'region_id': waterPrice.region_id, 'value': avgWaterConsume * waterPrice.price} for waterPrice in waterPrices]

        return filteredCities if len(filteredCities) >= 0 else cities

    def __calculateClientLightPrice__(self, totalHours):
        statesPrice = InfoLightPrice.query.all()
        return [{'state_id': statePrice.state_id, 'price':round(totalHours * statePrice.price_kwh, 2)} for statePrice in statesPrice]

    def __calculateClientWaterPrice__(self, totalLtWater):
        regionPrices = InfoWaterPriceRegion.query.all()
        return [{'region_id': regionPrice.region_id, 'price': round(regionPrice.price * totalLtWater, 2)} for regionPrice in regionPrices]

    def __calculateFormResultCostLiving__(self, formResult, att):
        allValues = list(map(lambda res: res.costLivingAttJson()[att], formResult))
        allValues = list(filter(lambda val: val != None, allValues))
        amountNonZeroesRes = list(filter(lambda res: res.costLivingAttJson()[att] != 0, formResult))
        total = ft.reduce(lambda a, b: a + b, allValues)
        return 0 if len(amountNonZeroesRes) == 0 else total/len(amountNonZeroesRes)