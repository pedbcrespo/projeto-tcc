from configuration.config import ormDatabase as orm

class InfoSchools(orm.Model):
    __tablename__ = 'info_schools'
    
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'), primary_key=True)
    amount_schools = orm.Column(orm.Float)
    scholarity_rate = orm.Column(orm.Float)
    
    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'amount_schools': self.amount_schools}