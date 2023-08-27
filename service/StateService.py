from model.State import State
from typing import List
from configuration.config import ormDatabase
import requests
from configuration.dev_configuration import IBGE_BASE_URL

class StateService:
    def getStates(self):
        states = State.query.all()
        return states
    
    def getStateByUf(self, uf):
        state = State.query.filter(State.abbreviation == uf).all()
        return state[0]
    
    def saveStates(self, states:List[State]):
        ormDatabase.session.add_all(states)
        ormDatabase.session.commit()
        return states