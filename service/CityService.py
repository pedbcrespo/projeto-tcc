from model.City import City
from model.State import State
from service.InfoService import InfoService
from configuration.config import ormDatabase
from typing import List

class CityService:
    def __getDetails__(self, city):
        infoService = InfoService()
        json = city.json()
        json.update(infoService.getDetailsInfo(city.id))
        return json
    
    def getAllCities(self):
        infoService = InfoService() 
        cities = City.query.all()
        jsonCities = [city.json() for city in cities]
        for city in jsonCities:
            info = infoService.getCityInfo(city['id'])
            city.update(info)
        return jsonCities
    
    def getCities(self, uf):
        infoService = InfoService() 
        state = State.query.filter(State.abbreviation == uf).first()
        cities = City.query.filter(City.state_id == state.id).all()
        jsonCities = []
        for city in cities:
            jsonCity = city.json()
            jsonCity.update(infoService.getDetailsInfo(city.id))
            jsonCities.append(jsonCity)
        return jsonCities 
    
    def getCityById(self, cityId):
        city = City.query.filter(City.id == cityId).first()
        return self.__getDetails__(city)
        
    def getCityByName(self, cityName):
        city = City.query.filter(City.name == cityName).first()
        return self.__getDetails__(city)
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return [city.json() for city in cities] 