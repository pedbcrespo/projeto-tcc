from configuration.config import ormDatabase as orm

class InfoGeneral(orm.Model):
    __tablename__ = 'info_general'
    
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'), primary_key=True)
    idh = orm.Column(orm.Float)
    population = orm.Column(orm.Integer)
    demographic_density = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'idh':self.idh, 'population': self.population, 'demographic_density': self.demographic_density}