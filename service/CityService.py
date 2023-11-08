from model.City import City
from model.State import State
from model.InfoSecurity import InfoSecurity
from model.InfoSchools import InfoSchools
from model.InfoGeneral import InfoGeneral
from model.InfoPrices import InfoPrices
from configuration.config import ormDatabase, statisticsFunction
from typing import List
import pandas as pd
import requests

class CityService:
    def getAllCities(self):
        cities = City.query.all()
        cities = [self.setDistricts(city) for city in cities]
        return [city for city in cities]
    
    def getCities(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
        dataframe = self.readingStateCsv(state.abbreviation.lower())
        cities = City.query.filter(City.state_id == state.id).all()
        cities = [self.setDetailsInfo(city, state, dataframe) for city in cities]
        return [city for city in cities] 
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return [city.json() for city in cities] 

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