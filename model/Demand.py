from configuration.config import ormDatabase

orm = ormDatabase

class Demand(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    description = orm.Column(orm.String(500))
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.description})"
    
    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}