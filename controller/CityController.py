from flask_restful import Resource
from configuration.config import api
from service.CityService import CityService

baseUrl = '/cities'

class CityController(Resource):
    service = CityService()
    def get(self):
        return self.service.getCities()

    def post(self, jsonCities):
        return self.service.saveCities(jsonCities['cities'])
    
api.add_resource(CityController, baseUrl)