from configuration.config import ormDatabase

class Region(ormDatabase.Model):
    id = ormDatabase.Column(ormDatabase.Integer, primary_key=True)
    name = ormDatabase.Column(ormDatabase.String(45))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"({self.id}, {self.name})"

    def json(self):
        return {'id': self.id, 'name': self.name}