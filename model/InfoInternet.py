from configuration.config import ormDatabase as orm

class InfoInternet(orm.Model):
    __tablename__ = 'info_internet'
    
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'), primary_key=True)
    avg_price = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'avg_price': self.avg_price}