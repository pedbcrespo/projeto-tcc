from configuration.config import ormDatabase

orm = ormDatabase

class District(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    city_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('city.id'))
    def __init__(self, name, cityId):
        self.name = name
        self.city_id = cityId
        
    def json(self):
        return {'id': self.id, 'name': self.name}