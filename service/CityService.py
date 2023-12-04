from model.City import City
from model.State import State
from model.InfoSecurity import InfoSecurity
from model.InfoSchools import InfoSchools
from model.InfoGeneral import InfoGeneral
from model.InfoPrices import InfoPrices
from configuration.config import ormDatabase
from typing import List

class CityService:
    def getAllCities(self):
        cities = City.query.all()
        cities = [self.setDistricts(city) for city in cities]
        return [city for city in cities]
    
    def getCities(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
        dataframe = self.readingStateCsv(state.abbreviation.lower())
        cities = City.query.filter(City.state_id == state.id).all()
        return [city for city in cities] 
    
    def getCityById(self, cityId):
        city = City.query.filter(City.id == cityId).first()
        return city.json()
    
    def getCityByName(self, cityName):
        city = City.query.filter(City.name == cityName).first()
        return city.json()
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return [city.json() for city in cities] 