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
from model.InfoAlimentation import InfoAlimentation
from model.InfoRecreation import InfoRecreation
from model.InfoHealthConsumer import InfoHealthConsumer
from model.FormAtributes import FormAttributes
import functools as ft
from typing import List

class InfoService:   
    def getRecomendation(self, formAttributes: FormAttributes):
        pass
    
    
    def __getInfo__(self, cityId, infoType):
        info = infoType.query.filter(infoType.city_id == cityId).first()
        return info.json()
    
    def getCityInfo(self, cityId):
        city = City.query.filter(City.id == cityId).first()
        info = {}
        info.update(self.__getInfo__(cityId, InfoGeneral))
        info.update(self.__getInfo__(cityId, InfoPrices))
        info.update(self.__getInfo__(cityId, InfoSecurity))
        info.update(self.__getInfo__(cityId, InfoSchools))
        info.update(self.getCoustLivingPrice(city))
        return info
    
    def getCoustLivingPrice(self, city):
        coust = self.__getCityCoustLiving__(city)
        return {'city_id': city.id, 'avg_coust_living_price': coust}
    
    def __getStates__(self):
        return State.query.all()
    
    def __getCityCoustLiving__(self, city:City):
        cousts = [
            self.__calculatingLightPriceConsumer__(city.state_id),
            self.__calculatingWaterPriceConsumer__(city.state_id),
            (InfoInternet.query.filter(InfoInternet.city_id == city.id).first()).avg_price,
            (InfoAlimentation.query.filter(InfoAlimentation.state_id == city.state_id).first()).avg_price,
            (InfoRecreation.query.filter(InfoRecreation.state_id == city.state_id).first()).avg_price,
            (InfoHealthConsumer.query.filter(InfoHealthConsumer.state_id == city.state_id).first()).avg_price
        ]
        return round(ft.reduce(lambda a, b: a+b, cousts), 2) 
        
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
        
    def __calculatingLightPriceConsumer__(self, stateId):
        price = InfoLightPrice.query.filter(InfoLightPrice.state_id == stateId).first()
        consumer = InfoLightConsume.query.filter(InfoLightConsume.state_id == stateId).first()
        mounthConsumerInHours = consumer.amount/12
        return round(mounthConsumerInHours*price.price_kwh, 2)
    
    def __calculatingWaterPriceConsumer__(self, stateId):
        state = State.query.filter(State.id == stateId).first()
        regionId = state.region_id
        regionPrice = InfoWaterPriceRegion.query.filter(InfoWaterPriceRegion.region_id == regionId).first()
        mounthCounsumer = InfoWaterConsumer.query.filter(InfoWaterConsumer.state_id == stateId).first()
        return round(mounthCounsumer.amount * regionPrice.price, 2)
        
        
        