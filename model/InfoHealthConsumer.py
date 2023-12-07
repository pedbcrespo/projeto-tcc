from configuration.config import ormDatabase as orm

class InfoHealthConsumer(orm.Model):
    __tablename__ = 'info_health_consumer'
    
    state_id = orm.Column(orm.Integer, orm.ForeignKey('state.id'), primary_key=True)
    avg_price = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'state_id': self.state_id, 'avg_price': self.avg_price}