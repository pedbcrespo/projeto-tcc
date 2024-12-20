from flask_restful import Resource
from flask import redirect, request, render_template, make_response
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.CityService import CityService
from service.InfoService import InfoService
from service.StateService import StateService
from service.RecomendationService import RecomendationService

cityService = CityService()
stateService = StateService()
infoService = InfoService()
recomendationService = RecomendationService()

class Initial(Resource):
    def get(self):
        return make_response(render_template('index.html'))

class RedirectToCities(Resource):
    def get(self):
        return redirect(BASE_URL)

class CityAllController(Resource):
    def get(self):
        return cityService.getAllCities()

class CityIndividualController(Resource):
    def get(self, uf):
        return [city for city in cityService.getCities(uf)]

class InfoCityController(Resource):
    def get(self, city_id):
        info = infoService.getCityInfo(city_id)
        return info
    
class CompleteCityInfo(Resource):
    def get(self, cityId):
        city = cityService.getCityById(cityId)
        city['info'] = infoService.getCityInfo(cityId)
        return city
    
class Recomendation(Resource):
    def post(self):
        formResult = request.json
        cities = recomendationService.getRecomendation(formResult)
        return cities
    
api.add_resource(RedirectToCities, "/")
api.add_resource(Initial, BASE_URL)
api.add_resource(CityAllController, f"{BASE_URL}/cities")
api.add_resource(CityIndividualController, f"{BASE_URL}/state/<uf>")
api.add_resource(InfoCityController, f"{BASE_URL}/city/info/<int:city_id>")
api.add_resource(Recomendation, f"{BASE_URL}/city/recomendation")
