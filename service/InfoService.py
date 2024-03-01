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
        info = {}
        info.update(self.getGeneralInfo(cityId))
        return info
    
    def getDetailsInfo(self, cityId):
        info = {}
        city = City.query.filter(City.id == cityId).first()
        info.update(self.getIdh(cityId))
        info.update(self.getPricesInfo(cityId))
        info.update(self.getCoustLivingPrice(city))
        info.update(self.getTopEnterprises(cityId))
        info.update(self.getEntertainmentEnterprisesAmount(cityId))
        info.update(self.getProfissionalQualificationRate(cityId))
        return info
    
    def getGeneralInfo(self, cityId):
        try:
            generalInfo = self.__getInfo__(cityId, InfoGeneral)
        except:
            generalInfo = {'demographic_density': None, 'population': None}
        return {'demographic_density': generalInfo['demographic_density'], 'population': generalInfo['population']}

    def getSecurityInfo(self, cityId):
        try:
            secInfo = self.__getInfo__(cityId, InfoSecurity)
            generalInfo = self.__getInfo__(cityId, InfoGeneral)
            securityRate = (secInfo['rate']/generalInfo['population'])*1000
            return {'security_rate': 1 - securityRate}
        except:
            return {'security_rate': None}
        
    def getScholarityInfo(self, cityId):
        try:
            scholarityInfo = self.__getInfo__(cityId, InfoSchools)
            return {'scholarity_rate': scholarityInfo['scholarity_rate']/10}
        except:
            return {'scholarity_rate': None}

    def getCoustLivingPrice(self, city):
        coust = self.__getCityCoustLiving__(city)
        return {'avg_coust_living_price': coust}
    
    def getPricesInfo(self, cityId):
        try:
            prices = self.__getInfo__(cityId, InfoPrices)
            return {'avg_price': prices['avg_price']}
        except:
            return {'avg_price': None}
        
    def getSanitationInfo(self, cityId):
        inversedRate = 0 
        sanitation = {'population_no_water': 0, 'population_no_sewage': 0, 'population_no_garbage_collection': 0 }
        try:
            sanitation = self.__getInfo__(cityId, InfoSanitation)
            for key in sanitation:
                if type(sanitation[key]) == str:
                    continue
                if sanitation[key] == None:
                    sanitation[key] = 100
        except:
            sanitation = InfoSanitation(cityId).json()
        inversedRate = (
            sanitation['population_no_water']/100 + 
            sanitation['population_no_sewage']/100 + 
            sanitation['population_no_garbage_collection']/100
        ) / 3
        return {'sanitation_rate': 1 - inversedRate}
        
    def getTopEnterprises(self, cityId):
        typeDescriptions = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).order_by(desc(InfoEnterprise.amount)).all()
        amounts = list(map(lambda enterprise: enterprise.amount, typeDescriptions))
        amount = 0 
        if len(amounts) > 0: 
            amount = ft.reduce(lambda a, b: a+b, amounts)
        justDesc = [info.type_description for info in typeDescriptions]
        return {'enterprises_amount': amount,'most_current_type_enterprises': justDesc[:5]}

    def getIdh(self, cityId):
        scholarityRate = self.getScholarityInfo(cityId)['scholarity_rate']
        securityRate = self.getSecurityInfo(cityId)['security_rate']
        sanitationRate = self.getSanitationInfo(cityId)['sanitation_rate']
        idh = (sanitationRate + securityRate + scholarityRate)/3
        return {'idh': round(idh, 3), 'scholarity_rate': round(scholarityRate, 2)}
    
    def __getCityCoustLiving__(self, city:City):
        coustLiving = InfoCoustLiving.query.filter(InfoCoustLiving.state_id == city.state_id).first()
        cousts = [
            self.__calculatingLightPriceConsumer__(city.state_id),
            self.__calculatingWaterPriceConsumer__(city.state_id),
            (InfoInternet.query.filter(InfoInternet.city_id == city.id).first()).avg_price,
            (coustLiving.alimentation),
            (coustLiving.transport),
            (coustLiving.health),
            (coustLiving.hygiene),
            (coustLiving.recreation),
        ]
        return round(ft.reduce(lambda a, b: a+b, cousts), 2) 
    
    def getEntertainmentEnterprisesAmount(self, cityId):
        def isEntertainmentEnterprise(enterprise):
            entertaimentWords = ['restaurante', 'lanchonete', 'cinema', 'bares', 'condicionamento fisico', 'passeio', 'turistico']
            type_description = unidecode.unidecode(enterprise.type_description).lower()
            for word in entertaimentWords:
                if word in type_description:
                    return True
            return False
        
        enterprises = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).all()
        filteredEnterprises = list(filter(lambda enterprise: isEntertainmentEnterprise(enterprise), enterprises))

        if not filteredEnterprises:
            return {'recreation_rate': 0}

        amountsEnterprises = list(map(lambda enterprise: enterprise.amount, filteredEnterprises))
        amountEntertaimentEnterprises = ft.reduce(lambda a, b: a+b, amountsEnterprises)
        enterprisesAmounts = list(map(lambda enterprise: enterprise.amount, enterprises))
        totalAmount = ft.reduce(lambda a, b: a+b, enterprisesAmounts)
        amount = amountEntertaimentEnterprises / totalAmount
        return {'recreation_rate': round(amount*100, 2)}

    def getProfissionalQualificationRate(self, cityId):
        general = InfoGeneral.query.filter(InfoGeneral.city_id == cityId).first()
        enterprises = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).all()
        if not enterprises:
            return {'business_accessibility': 0}
        amountEnterprises = ft.reduce(lambda a,b: a+b, list(map(lambda enterprise: enterprise.amount, enterprises)))
        businessAccessibility = amountEnterprises/general.population
        return {'business_accessibility': round(businessAccessibility*100, 2)}


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
        
        
        