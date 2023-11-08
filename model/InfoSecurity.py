from configuration.config import ormDatabase as orm

class InfoSecurity(orm.Model):
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'))
    security_rate = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'security_rate': self.security_rate}