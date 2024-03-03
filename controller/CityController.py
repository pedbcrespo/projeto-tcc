from flask_restful import Resource
from flask import redirect
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.CityService import CityService
from service.InfoService import InfoService
from service.StateService import StateService

cityService = CityService()
stateService = StateService()
infoService = InfoService()

class Initial(Resource):
    def get(self):
        return "API TCC"

class RedirectToCities(Resource):
    def get(self):
        return redirect(BASE_URL)

class CityAllController(Resource):
    def get(self):
        return cityService.getAllCities()

    def post(self, jsonCities):
        return [city for city in cityService.saveCities(jsonCities['cities'])]

class CityIndividualController(Resource):
    def get(self, uf):
        return [city for city in cityService.getCities(uf)]

class InfoCityController(Resource):
    def get(self, city_id):
        return infoService.getCityInfo(city_id)
    
class CompleteCityInfo(Resource):
    def get(self, cityId):
        city = cityService.getCityById(cityId)
        city['info'] = infoService.getCityInfo(cityId)
        return city
api.add_resource(RedirectToCities, "/")
api.add_resource(Initial, BASE_URL)
api.add_resource(CityAllController, f"{BASE_URL}/cities")
api.add_resource(CityIndividualController, f"{BASE_URL}/state/<uf>")
api.add_resource(InfoCityController, f"{BASE_URL}/city/info/<int:city_id>")
