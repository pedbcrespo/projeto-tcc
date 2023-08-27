from model.City import City
from configuration.config import ormDatabase
from configuration.dev_configuration import IBGE_BASE_URL
from model.State import State
from typing import List
import requests

class CityService:
    def getAllCities(self):
        cities = City.query.all()
        return cities
    
    def getCityById(self, cityId):
        city = City.query.filter(City.id == cityId).all()
        return city[0]
    
    def getCitiesOfState(self, state:State):
        cities = City.query.filter(City.state_id == state.id).all()
        if len(cities) > 0:
            return cities
        uf = state.abbreviation
        response = requests.get(f"{IBGE_BASE_URL}/estados/{uf}/municipios")
        cities = [City(city['nome'], state.id) for city in response.json()]
        return cities
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return cities