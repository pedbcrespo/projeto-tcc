from model.State import State
from configuration.config import ormDatabase

class StateService:
    def getStates(self):
        states =  State.query.all()
        return {"data": [{"id": state.id, "name": state.name, "abbreviation": state.abbreviation} for state in states]}
    
    def saveStates(self, states):
        ormDatabase.session.add_all(states)
        ormDatabase.session.commit()
        
        return {'states':states}