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

from configuration.config import ormDatabase, statisticsFunction
from typing import List

class InfoService:
    def getRecomendation(self, formAttributes):
        pass
    
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