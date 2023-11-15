from configuration.config import ormDatabase as orm

class InfoLightConsume(orm.Model):
    state_id = orm.Column(orm.Integer, orm.ForeignKey('state.id'), primary_key=True)
    amount = orm.Column(orm.Float)

    def __init__(self, stateId):
        self.city_state_idid = stateId
        
    def json(self):
        return {'state_id': self.state_id, 'amount': self.amount}

