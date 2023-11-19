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
from model.FormAtributes import FormAttributes

from configuration.config import ormDatabase, statisticsFunction
from typing import List

class InfoService:
    def __init__(self):
        self.states = State.query.all()
    
    def getRecomendation(self, formAttributes: FormAttributes):
        recomendation = []
        citiesByHomePrices = self.__gettingHomePrices__(formAttributes.priceRate)
        citiesWithChooseSize = self.__gettingCitiesBySize__(formAttributes.typeCitySize)
        citiesByCoustLivinPrices = self.__gettingCoustLiving__(formAttributes.coustLivingPriceRate)
        
        return recomendation
    
    def getInfo(self, cityId, infoType):
        info = infoType.query.filter(infoType.city_id == cityId).first()
        return info.json()
    
    def getCityInfo(self, cityId):
        info = {}
        info.update(self.getInfo(cityId, InfoGeneral))
        info.update(self.getInfo(cityId, InfoPrices))
        info.update(self.getInfo(cityId, InfoSecurity))
        info.update(self.getInfo(cityId, InfoSchools))
        return info
    
    def __gettingHomePrices__(self, price):
        prices = InfoPrices.query.filter(InfoPrices.avg_price <= price)
        citiesIds = list(map(lambda infoPrice: infoPrice.city_id, prices))
        cities = City.query.filter(City.id in citiesIds).all()
        
        def unionCityData(infoPrice):
            city = list(filter(lambda x: x.id == infoPrice.city_id, cities))
            return {'city': city, 'avgPrice': infoPrice.avg_price}
        
        return list(map(lambda infoPrice: unionCityData(infoPrice), prices))
    
    def __gettingCitiesBySize__(self, size):
        typeSizeCities = InfoGeneral.query.filter(InfoGeneral.population >= size['min'] and InfoGeneral.population <= size['max'])
        citiesIds = list(map(lambda x: x.city_id, typeSizeCities))
        cities = City.query.filter(City.id in citiesIds).all()
        
        def unionCityData(infoGeneral):
            city = list(filter(lambda x: x.id == infoGeneral.city_id, cities))
            return {'city': city, 'population': infoGeneral.population}
        
        return list(map(lambda infoGeneral: unionCityData(infoGeneral), typeSizeCities))
    
    def __gettingCoustLiving__(self, coustLivingPrice):
        for state in self.states:
            lightPrice = self.__calculatingLightPriceConsumer_(state)
            waterPrice = self.__calculatingWaterPriceConsumer__(state)
            cities = City.query.filter(City.state_id == state.id).all()
            
            correspondetCoustLivingPriceCities = []
            for city in cities:
                internetPrice = InfoInternet.query.filter(InfoInternet.city_id == city.id).first()
                sumPrices = internetPrice + lightPrice + waterPrice
                if sumPrices <= coustLivingPrice:
                    correspondetCoustLivingPriceCities.append({'city': city, 'price': sumPrices})
        
        return correspondetCoustLivingPriceCities
            
            
    def __calculatingLightPriceConsumer_(self, state):
        stateId = state.id
        yearInHours = 8760
        price = InfoLightPrice.query.filter(InfoLightPrice.state_id == stateId).first()
        consumer = InfoLightConsume.query.filter(InfoLightConsume.state_id == stateId).first()
        
        yearConsumerInHours = consumer/yearInHours
        mounthConsumerInHours = yearConsumerInHours/12
        return round(mounthConsumerInHours*price, 2)
    
    def __calculatingWaterPriceConsumer__(self, state):
        regionId = state.region_id
        regionPrice = InfoWaterPriceRegion.query.filter(InfoWaterPriceRegion.region_id == regionId).first()
        dailyConsumer = InfoWaterConsumer.query.filter(InfoWaterConsumer.state_id == state.id).first()
        mounthCounsumer = dailyConsumer*30
        return round(mounthCounsumer * regionPrice, 2)
        
        
        