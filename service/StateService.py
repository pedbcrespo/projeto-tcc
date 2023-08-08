from model.State import State
from configuration import config

class StateService:
    def getStates(self):
        states =  State.query.all()
        return {"data": [{"id": state.id, "name": state.name, "abbreviation": state.abbreviation} for state in states]}