from configuration import  dev_configuration
from model.City import City
from service.StateService import StateService
from service.CityService import CityService
from configuration.config import ormDatabase
import requests

orm = ormDatabase
url = 'https://servicodados.ibge.gov.br/api/v1/localidades'


def getStates():
    response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    return response.json()

def getCitiesOfState(uf):
    response = requests.get(f"{url}/estados/{uf}/municipios")
    return response.json()


def saveCities():
    stateService = StateService()
    cityService = CityService()
    states = stateService.getStates()
    for state in states:
        cities = [City(city['nome'], state['id']) for city in getCitiesOfState(state.abbreviation)]
        cityService.saveCities(cities)