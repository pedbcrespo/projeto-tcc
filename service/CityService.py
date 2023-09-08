from model.City import City
from model.State import State
from model.District import District
from configuration.config import ormDatabase
from configuration.dev_configuration import IBGE_BASE_URL
from typing import List
import requests

class CityService:
    def getAllCities(self):
        cities = City.query.all()
        cities = [self.setDistricts(city) for city in cities]
        return [city for city in cities]
    
    def getCityById(self, cityId):
        city = City.query.filter(City.id == cityId).first()
        city = self.setDistricts(city)
        return city
    
    def getCitiesOfState(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
        cities = City.query.filter(City.state_id == state.id).all()
        cities = [self.setDistricts(city) for city in cities]
        return [city for city in cities] 
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return [city.json() for city in cities] 
    
    def setDistricts(self, city:City):
        districts = District.query.filter(District.city_id == city.id).all()
        city.districts = districts
        return city.json()