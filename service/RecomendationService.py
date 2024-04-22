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
from model.attributes import Attributes
from service.InfoService import InfoService
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft
from typing import List, Dict

class RecomendationService:
    infoService = InfoService()
    def getRecomendation(self, formResult):
        listformResultObj = list(map(lambda res: FormResult(res), formResult))
        attributePoints = self.__calculateAttributes__(listformResultObj)
        sortedListAttributes = sorted(attributePoints.getOrdenationAttributeList(), key=lambda att: att['value'], reverse=True)
        listAttributeKeys = list(map(lambda att: att['key'], sortedListAttributes))
        attributesHandleRelated = {
            Attributes.LIVING_QUALITY: self.__getBetterIdh__,
            Attributes.EMPLOYABILITY: self.__getBetterBusinessSAccessibility__,
            Attributes.LEISURE: self.__getBetterEntertainment__,
            Attributes.COST: self.__getBetterCoust__,
        }
        attributesKey = {
            Attributes.LIVING_QUALITY: 'idh',
            Attributes.EMPLOYABILITY: 'business_accessibility',
            Attributes.LEISURE : 'recreation_rate',
            Attributes.COST: 'total'
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
        generalPontuation : Dict[str, Dict] = {
            Attributes.HOURS_LIGHT_ESTIMATE: {'total': 0, 'count': 0},
            Attributes.LT_WATER_CONSUME: {'total': 0, 'count': 0},
            Attributes.ALIMENTATION: {'total': 0, 'count': 0},
            Attributes.HYGIENE: {'total': 0, 'count': 0},
            Attributes.TRANSPORTATION: {'total': 0, 'count': 0},
            Attributes.HEALTH: {'total': 0, 'count': 0},
            Attributes.RECREATION: {'total': 0, 'count': 0}
        }
        ordenationAttributes : Dict[str, int] = {
            Attributes.LIVING_QUALITY: 0,
            Attributes.EMPLOYABILITY: 0,
            Attributes.LEISURE: 0,
            Attributes.COST: 0,
        }
        for formatResult in listFormResult: 
            for key in formatResult.increase:
                ordenationAttributes[key] += formatResult.answer
        
            for key in formatResult.decrease:
                ordenationAttributes[key] -= formatResult.answer
                if ordenationAttributes[key] < 0:
                    ordenationAttributes[key] = 0

            for key in formatResult.pontuations:
                generalPontuation[key]['total'] += formatResult.getPontuation(key)
                generalPontuation[key]['count'] += 1
        
        for key in generalPontuation:
            total = generalPontuation[key]['total']
            count = generalPontuation[key]['count']
            generalPontuation[key]['avg'] = round(total/count, 2)
        print(generalPontuation)
        allInfoLightPrice = InfoLightPrice.query.all()
        allInfoWaterPrice = InfoWaterPriceRegion.query.all()
        lightPrices = list(map(lambda lightPrice: lightPrice.price_kwh , allInfoLightPrice))
        waterPrices = list(map(lambda waterPrice: waterPrice.price , allInfoWaterPrice))
        return AttributesPoints(ordenationAttributes, generalPontuation, lightPrices, waterPrices)
    
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
        allCities = City.query.all()
        cities = allCities
        citiesFiltered = self.__filteredCitiesByWaterAndLightConsume__(cities, attributesPoints)
        avgWaterConsume = attributesPoints.subAttributes[Attributes.LT_WATER_CONSUME]
        avgLightConsume = attributesPoints.subAttributes[Attributes.HOURS_LIGHT_ESTIMATE]
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
        avgLightConsume = attributesPoints.subAttributes[Attributes.HOURS_LIGHT_ESTIMATE]
        avgWaterConsume = attributesPoints.subAttributes[Attributes.LT_WATER_CONSUME]
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