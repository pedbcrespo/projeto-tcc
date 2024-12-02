from configuration.config import ormDatabase
from model.State import State
orm = ormDatabase

class City(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    state_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('state.id'))
    ibge_id = orm.Column(orm.Integer)
    
    def __init__(self, name, state_id):
        self.name = name
        self.state_id = state_id
                    
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.state_id})"
    
    def json(self, State: State = None):
        result = {'id': self.id, 'state_id':self.state_id, 'ibge_id': self.ibge_id}
        result['name'] = f"{self.name} - {State.abbreviation}" if State else self.name
        return result
