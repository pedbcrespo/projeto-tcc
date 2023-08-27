from . import config

orm = config.ormDatabase

class District(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    city_id = config.ormDatabase.Column(config.ormDatabase.Integer, config.ormDatabase.ForeignKey('city.id'))
    def __init__(self, name, cityId):
        self.name = name
        self.city_id = cityId