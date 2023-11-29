from configuration.config import ormDatabase as orm

class InfoSecurity(orm.Model):
    __tablename__ = 'info_security'
    
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'), primary_key=True)
    rate = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'rate': self.rate}