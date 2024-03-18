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
from sqlalchemy import desc
import functools as ft
import pandas as pd

class InfoService:
    def getQuestions(self):
        return questions

    def getRecomendation(self, formResult): 
        attributesPoints, df = self.__calculateAttributes__(formResult)
        listAttributes = sorted(attributesPoints.getList(), key=lambda att: att['value'])
        sortedAttributes = list(map(lambda att: att['key'], listAttributes))
        attributesHandleRelated = {
            'LIVING_QUALITY': self.__getBetterIdh__,
            'EMPLOYABILITY': self.__getBetterBusinessSAccessibility__,
            'LEISURE': self.__getBetterEntertainment__,
            'COUST': self.__getBetterCoust__,
        }
        attributesKey = {
            'LIVING_QUALITY': 'idh',
            'EMPLOYABILITY': 'business_accessibility',
            'LEISURE' : 'recreation_rate',
            'COUST': 'total'
        }
        cities = City.query.all()
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

        infos = []
        for city in sortedCities:
            dictCity = city.json()
            dictCity.update(self.getCityInfo(city.id))
            dictCity.update(self.getDetailsInfo(city.id))
            infos.append(dictCity)
        print(sortedCities, infos[0])
        return infos
    
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
        info.update(self.getEntertainmentRate(cityId))
        info.update(self.getProfissionalQualificationRate(cityId))
        return info
    
    def getGeneralInfo(self, cityId):
        try:
            generalInfo = self.__getInfo__(cityId, InfoGeneral)
        except:
            generalInfo = {'demographic_density': 0, 'population': 0}
        return {'demographic_density': generalInfo['demographic_density'], 'population': generalInfo['population']}

    def getSecurityInfo(self, cityId):
        try:
            secInfo = self.__getInfo__(cityId, InfoSecurity)
            generalInfo = self.__getInfo__(cityId, InfoGeneral)
            securityRate = round(secInfo['rate']/generalInfo['population'], 3)
            return {'security_rate': 1 - securityRate}
        except:
            return {'security_rate': 0}
        
    def getScholarityInfo(self, cityId):
        try:
            scholarityInfo = self.__getInfo__(cityId, InfoSchools)
            return {'scholarity_rate': scholarityInfo['scholarity_rate']/10}
        except:
            return {'scholarity_rate': 0}

    def getCoustLivingPrice(self, city):
        coust = self.__getCityCoustLiving__(city)
        return {'avg_coust_living_price': coust}
    
    def getPricesInfo(self, cityId):
        try:
            prices = self.__getInfo__(cityId, InfoPrices)
            return {'avg_price': prices['avg_price']}
        except:
            return {'avg_price': 0}
        
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
        return {'idh': round(idh, 3), 'scholarity_rate': round(scholarityRate, 2), 'securityRate': securityRate, 'sanitationRate': sanitationRate}
    
    def getEntertainmentRate(self, cityId):
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
        population = general.population
        city = City.query.filter(City.id == cityId).first()
        print('CIDADE: ', cityId, city.name, 'populacao nao encontrada.')
        enterprises = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).all()
        if not enterprises:
            return {'business_accessibility': 0}
        amountEnterprises = ft.reduce(lambda a,b: a+b, list(map(lambda enterprise: enterprise.amount, enterprises)))
        businessAccessibility = amountEnterprises/population
        return {'business_accessibility': round(businessAccessibility*100, 2)}

    def __calculateAttributes__(self, formResult):
        attributesPoints = AttributesPoints()
        for data in formResult:
            attributesPoints.add(data['increase'], data['decrease'], data['answer'])
        df = pd.DataFrame([attributesPoints.attributes])
        return attributesPoints, df

    def __getHomePrices__(self, price):
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
        
    def __getCityCoustLiving__(self, city):
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
    
    def __getTotalCoust__(self, cityId):
        city = City.query.filter(City.id == cityId).first()
        coustLiving = self.__getCityCoustLiving__(city)
        infoPrice = InfoPrices.query.filter(InfoPrices.city_id == cityId).first()
        avgHomesPrice = 0 if infoPrice == None else infoPrice.avg_price
        return {'total': round(avgHomesPrice + coustLiving, 2)}

    def __getInfo__(self, cityId, infoType):
        info = infoType.query.filter(infoType.city_id == cityId).first()
        return info.json()
    
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
        return self.__getBetter__(cities, self.getIdh, 'idh', qtd)
    
    def __getBetterBusinessSAccessibility__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.getProfissionalQualificationRate, 'business_accessibility', qtd)
    
    def __getBetterEntertainment__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.getEntertainmentRate, 'recreation_rate', qtd)
    
    def __getBetterCoust__(self, cities=None, qtd=10):
        return self.__getBetter__(cities, self.__getTotalCoust__, 'total', qtd, False)