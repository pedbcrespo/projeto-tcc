from model.State import State
from typing import List
from configuration.config import ormDatabase
from configuration.dev_configuration import IBGE_BASE_URL

class StateService:
    def getStates(self):
        states = State.query.all()
        return [state.json() for state in states]
    
    def saveStates(self, states:List[State]):
        ormDatabase.session.add_all(states)
        ormDatabase.session.commit()
        return states.json()