from configuration.config import ormDatabase as orm

class InfoSchools(orm.Model):
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'))
    avg_homes_price = orm.Column(orm.Float)
    scholarity_rate = orm.Column(orm.Float)
    
    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'avg_homes_price': self.avg_homes_price}