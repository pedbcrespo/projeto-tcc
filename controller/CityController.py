from flask_restful import Resource
from configuration.config import api
from service.CityService import CityService
from service.StateService import StateService

baseUrl = '/cities'

cityService = CityService()
stateService = StateService()

class CityAllController(Resource):
    def get(self):
        return [city for city in cityService.getAllCities()]

    def post(self, jsonCities):
        return [city for city in cityService.saveCities(jsonCities['cities'])]

class CityIndividualController(Resource):
    def get(self, uf):
        return [city for city in cityService.getCitiesOfState(uf)]
         
    
api.add_resource(CityAllController, baseUrl)
api.add_resource(CityIndividualController, f"{baseUrl}/<uf>")
