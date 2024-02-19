from configuration.config import ormDatabase as orm

class InfoEnterprise(orm.Model):
    __tablename__ = 'info_enterprises'
    id = orm.Column(orm.Integer, primary_key=True)
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'))
    amount = orm.Column(orm.Integer)
    type_description = orm.Column(orm.String)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'amount':self.amount, 'type_description': self.type_description}