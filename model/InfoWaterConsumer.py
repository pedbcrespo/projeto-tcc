from configuration.config import ormDatabase

class InfoWaterConsumer(ormDatabase.Model):
    __tablename__ = 'info_water_consumer'
    
    state_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('state.id'), primary_key=True)
    amount = ormDatabase.Column(ormDatabase.Float)

    def __repr__(self):
        return f"({self.state_id}, {self.amount})"

    def json(self):
        return {'state_id': self.state_id, 'amount': self.amount}