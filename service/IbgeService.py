from model.City import City
from model.State import State
from service.StateService import StateService
from service.CityService import CityService
from configuration.config import ormDatabase
from configuration.dev_configuration import IBGE_BASE_URL
import requests

class IbgeService:
    stateService = StateService()
    cityService = CityService()
    
    def getStates(self):
        response = requests.get(f"{IBGE_BASE_URL}/estados")
        states = [State(state['nome'], state['sigla']) for state in response.json()]
        return states
    
    def getCities(self, state):
        print(f"* {state.name}::{state.abbreviation}")
        uf = state.abbreviation
        response = requests.get(f"{IBGE_BASE_URL}/estados/{uf}/municipios")
        cities = [City(city['nome'], state.id) for city in response.json()]
        return cities
    
    
    def settingData(self):
        response = {}
        states = State.query.all()
        print('=================================')
        print(states)
        print('=================================')
        # states = self.getStates() if len(states) == 0 else states
        # self.stateService.saveStates(states)
        for state in states:
            cities = self.getCities(state)
            cities = self.cityService.saveCities(cities)
            response[state.name] = cities
        return response        

