from configuration.config import ormDatabase as orm
AVG_LIGHT_CONSUMER = 2362 #(kWh/hab)

class InfoLightPrice(orm.Model):
    __tablename__ = 'info_light_price'
    
    state_id = orm.Column(orm.Integer, orm.ForeignKey('state.id'), primary_key=True)
    price_kwh = orm.Column(orm.Float)

    def __init__(self, stateId):
        self.city_state_idid = stateId
        
    def json(self):
        return {'state_id': self.state_id, 'price_kwh': self.price_kwh}

