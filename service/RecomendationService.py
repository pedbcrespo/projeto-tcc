import json
import unidecode
from model.City import City
from model.State import State
from model.InfoSecurity import InfoSecurity
from model.InfoSchools import InfoSchools
from model.InfoGeneral import InfoGeneral
from model.InfoPrices import InfoPrices
from model.InfoLightConsume import InfoLightConsume
from model.InfoLightPrice import InfoLightPrice
from model.InfoWaterConsumer import InfoWaterConsumer
from model.InfoWaterPriceRegion import InfoWaterPriceRegion
from model.InfoInternet import InfoInternet
from model.InfoCoustLiving import InfoCoustLiving
from model.InfoSanitation import InfoSanitation
from model.InfoEnterprise import InfoEnterprise
from model.Questions import AttributesPoints, questions
from model.FormResult import FormResult
from service.InfoService import InfoService
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft

class RecomendationService:
    infoService = InfoService()
    def getRecomendation(self, formResult):
        listformResultObj = list(map(lambda res: FormResult(res), formResult))
        attributesPoints = self.__calculateAttributes__(listformResultObj)
        listAttributes = sorted(attributesPoints.getList(), key=lambda att: att['value'], reverse=True)
        sortedAttributes = list(map(lambda att: att['key'], listAttributes))
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
        cities = self.__getCitiesToRecomendation__(attributesPoints)
        print(formResult)
        print('Attributes points:', attributesPoints)
        print(formResult)
        print('================================')
        print(sortedAttributes)
        for att in sortedAttributes:
            print('================================')
            print('analisando: ', att)
            cities = attributesHandleRelated[att](cities)
        print('================================')

        def handleSortedCity(city):
            listAtt = [city.infoValue[attributesKey[att]] for att in sortedAttributes]
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

    def __calculateAttributes__(self, listFormResult):
        attributesPoints = AttributesPoints()
        totalRelated = {
            'hoursLightEstiamte': 'totalLightHours',
            'ltWaterConsume': 'totalLtWater',
        }
        totals = {
            'totalLightHours': 0,
            'totalLtWater': 0
        }
        totalCostLiving = 0

        for data in listFormResult:
            attributesPoints.add(data.increase, data.decrease, data.answer)

        for att in listFormResult[0].costLivingAttJson():
            if att in ['hoursLightEstiamte', 'ltWaterConsume']:
                totals[totalRelated[att]] = self.__calculateFormResultCostLiving__(listFormResult, att)
            totalCostLiving += self.__calculateFormResultCostLiving__(listFormResult, att)

        attributesPoints.pricesLight = self.__calculateClientLightPrice__(totals['totalLightHours'])
        attributesPoints.pricesWater = self.__calculateClientWaterPrice__(totals['totalLtWater'])
        attributesPoints.limitCoustLiving = totalCostLiving
        return attributesPoints
    
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
    
    def __getCitiesToRecomendation__(self, attributesPoints):
        cities = City.query.all()
        citiesFiltered = self.__filteredCitiesByWaterAndLightPriceConsume__(cities, attributesPoints)
        with self.__createSession__() as session:
            query = session.query(
                City.id.label('city_id'),
                State.id.label('state_id'),
                (
                    func.round(InfoWaterPriceRegion.price * InfoWaterConsumer.amount, 2) +
                    func.round((InfoLightConsume.amount / 12) * InfoLightPrice.price_kwh, 2) +
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
            filteredResults = list(filter(lambda result: result[2] <= attributesPoints.getTotal(), results))
            filteredResultsCityIds = list(map(lambda result: result[0], filteredResults))
            cities = list(filter(lambda city: city.id in filteredResultsCityIds, citiesFiltered))
        return cities
    
    def __filteredCitiesByWaterAndLightPriceConsume__(self, cities, attributesPoints):
        lightPrices = list(map(lambda att: att['price'], attributesPoints.pricesLight))
        waterPrices = list(map(lambda att: att['price'], attributesPoints.pricesWater))
        handleAvg =lambda numberList: ft.reduce(lambda a, b: a+b, numberList)
        avgLight = handleAvg(lightPrices)
        avgWater = handleAvg(waterPrices)
        
        with self.__createSession__() as session:
            query = session.query(
                State.id.label('state_id'),
                func.round(InfoWaterPriceRegion.price * InfoWaterConsumer.amount, 2).label('avg_water_price'),
                func.round((InfoLightConsume.amount / 12) * InfoLightPrice.price_kwh, 2).label('avg_light_price')
            ).join(InfoWaterPriceRegion, State.region_id == InfoWaterPriceRegion.region_id
            ).join(InfoWaterConsumer, InfoWaterConsumer.state_id == State.id
            ).join(InfoLightPrice, InfoLightPrice.state_id == State.id
            ).join(InfoLightConsume, InfoLightConsume.state_id == State.id)
            results = query.all()
            filteredStates = list(filter(lambda res: res[1] <= avgWater and res[2] <= avgLight, results))
            stateIds = list(map(lambda filteredResult: filteredResult[0], filteredStates))
            filteredCities = list(filter(lambda city: city.state_id in stateIds, cities))
            return filteredCities

    def __calculateClientLightPrice__(self, totalHours):
        statesPrice = InfoLightPrice.query.all()
        return [{'state_id': statePrice.state_id, 'price':round(totalHours * statePrice.price_kwh, 2)} for statePrice in statesPrice]

    def __calculateClientWaterPrice__(self, totalLtWater):
        regionPrices = InfoWaterPriceRegion.query.all()
        return [{'region_id': regionPrice.region_id, 'price': round(regionPrice.price * totalLtWater, 2)} for regionPrice in regionPrices]

    def __calculateFormResultCostLiving__(self, formResult, att):
        allValues = list(map(lambda res: res.costLivingAttJson()[att], formResult))
        allValues = list(filter(lambda val: val != None, allValues))
        print('ALL VALUES', allValues)
        amountNonZeroesRes = list(filter(lambda res: res.costLivingAttJson()[att] != 0, formResult))
        total = ft.reduce(lambda a, b: a + b, allValues)
        return 0 if len(amountNonZeroesRes) == 0 else total/len(amountNonZeroesRes)