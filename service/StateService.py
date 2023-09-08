from model.State import State
from typing import List
from configuration.config import ormDatabase
import requests
from configuration.dev_configuration import IBGE_BASE_URL

class StateService:
    def getStates(self):
        states = State.query.all()
        return [state.json() for state in states]
    
    def getStateByUf(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
        return state.json()
    
    def saveStates(self, states:List[State]):
        ormDatabase.session.add_all(states)
        ormDatabase.session.commit()
        return states.json()