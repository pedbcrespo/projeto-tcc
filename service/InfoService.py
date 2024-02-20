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
from model.InfoSanitation import InfoSanitation
from model.InfoEnterprise import InfoEnterprise
from model.FormAtributes import FormAttributes
from sqlalchemy import desc
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
        info = {'id':city.id, 'city': city.name}
        info.update(self.getIdh(cityId))
        info.update(self.getPricesInfo(cityId))
        info.update(self.getCoustLivingPrice(city))
        info.update(self.getTopEnterprises(cityId))
        return info
    
    def getGeneralInfo(self, cityId):
        generalInfo = self.__getInfo__(cityId, InfoGeneral)
        return {'idh': generalInfo['idh'], 'population': generalInfo['population']}

    def getSecurityInfo(self, cityId):
        secInfo = self.__getInfo__(cityId, InfoSecurity)
        generalInfo = self.__getInfo__(cityId, InfoGeneral)
        securityRate = (secInfo['rate']/generalInfo['population'])*1000
        return {'security_rate': 1 - securityRate}

    def getScholarityInfo(self, cityId):
        scholarityInfo = self.__getInfo__(cityId, InfoSchools)
        return {'scholarity_rate': scholarityInfo['scholarity_rate']/10}

    def getCoustLivingPrice(self, city):
        coust = self.__getCityCoustLiving__(city)
        return {'avg_coust_living_price': coust}
    
    def getPricesInfo(self, cityId):
        prices = self.__getInfo__(cityId, InfoPrices)
        return {'avg_price': prices['avg_price']}
    
    def getSanitationInfo(self, cityId):
        sanitation = self.__getInfo__(cityId, InfoSanitation)
        inversedRate = 0 
        for key in sanitation:
            if type(sanitation[key]) == str:
                continue
            if sanitation[key] == None:
                sanitation[key] = 100
    
        inversedRate = (
            sanitation['population_no_water']/100 + 
            sanitation['population_no_sewage']/100 + 
            sanitation['population_no_garbage_collection']/100
        ) / 3
        return {'sanitation_rate': 1 - inversedRate}

    def getTopEnterprises(self, cityId):
        typeDescriptions = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).order_by(desc(InfoEnterprise.amount)).all()
        justDesc = [info.type_description for info in typeDescriptions]
        return {'most_current_type_enterprises': justDesc[:10]}

    def getIdh(self, cityId):
        scholarityRate = self.getScholarityInfo(cityId)['scholarity_rate']
        securityRate = self.getSecurityInfo(cityId)['security_rate']
        sanitationRate = self.getSanitationInfo(cityId)['sanitation_rate']
        idh = (sanitationRate + securityRate + scholarityRate)/3
        return {'idh': round(idh, 3)}
    
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
        
        
        