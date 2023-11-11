from flask_restful import Resource
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.CityService import CityService
from service.StateService import StateService

cityService = CityService()
stateService = StateService()

class CityAllController(Resource):
    def get(self):
        return [city for city in cityService.getAllCities()]

    def post(self, jsonCities):
        return [city for city in cityService.saveCities(jsonCities['cities'])]

class CityIndividualController(Resource):
    def get(self, uf):
        return [city for city in cityService.getCities(uf)]
         
class InfoCity(Resource):
    def get(self, cityId):
        return cityService.getCityInfo(cityId)
    
api.add_resource(CityAllController, BASE_URL)
api.add_resource(CityIndividualController, f"{BASE_URL}/states/<uf>")
