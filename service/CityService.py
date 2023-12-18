from model.City import City
from model.State import State
from service.InfoService import InfoService
from configuration.config import ormDatabase
from typing import List

class CityService:
    def getAllCities(self):
        infoService = InfoService() 
        cities = City.query.all()
        jsonCities = [city.json() for city in cities]
        return jsonCities
    
    def getCities(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
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