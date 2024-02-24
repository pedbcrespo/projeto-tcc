from configuration.config import ormDatabase as orm

class InfoCoustLiving(orm.Model):
    __tablename__ = 'info_coust_living'
    
    state_id = orm.Column(orm.Integer, orm.ForeignKey('state.id'), primary_key=True)
    alimentation = orm.Column(orm.Float)
    transport = orm.Column(orm.Float)
    health = orm.Column(orm.Float)
    hygiene = orm.Column(orm.Float)
    recreation = orm.Column(orm.Float)

    def __init__(self, stateId):
        self.city_state_idid = stateId
        
    def json(self):
        return {
            'state_id': self.state_id,
            'alimentation': self.alimentation, 
            'transport': self.transport, 
            'healf': self.health, 
            'hygiene': self.hygiene,
            'recreation': self.recreation
        }

