from configuration.config import ormDatabase

class State(ormDatabase.Model):
    id = ormDatabase.Column(ormDatabase.Integer, primary_key=True)
    ibge_id = ormDatabase.Column(ormDatabase.Integer) 
    name = ormDatabase.Column(ormDatabase.String(100))
    abbreviation = ormDatabase.Column(ormDatabase.String(2))
    region_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('region.id'))
    
    def __init__(self, name, abbreviation, region_id):
        self.name = name
        self.abbreviation = abbreviation
        self.region_id = region_id

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.abbreviation}, {self.region_id}, {self.ibge_id})"

    def json(self):
        return {'id': self.id, 'name': self.name, 'abbreviation': self.abbreviation, 'region_id': self.region_id, 'ibge_id': self.ibge_id}