from configuration.config import ormDatabase as orm

class InfoGeneral(orm.Model):
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'))
    idh = orm.Column(orm.Float)
    pib_per_capta = orm.Column(orm.Float)
    population = orm.Column(orm.Integer)
    demographic_density = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {'city_id': self.city_id, 'idh':self.idh, 'pib_per_capta': self.pib_per_capta, 'population': self.population, 'demographic_density': self.demographic_density}