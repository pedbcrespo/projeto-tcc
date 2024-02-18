from configuration.config import ormDatabase as orm

class InfoSanitation(orm.Model):
    __tablename__ = 'info_sanitation'
    id = orm.Column(orm.Integer, primary_key=True)
    city_id = orm.Column(orm.Integer, orm.ForeignKey('city.id'), primary_key=True)
    has_municipal_plan = orm.Column(orm.String)
    population_no_water = orm.Column(orm.Float)
    population_no_sewage = orm.Column(orm.Float)
    population_no_garbage_collection = orm.Column(orm.Float)

    def __init__(self, cityId):
        self.city_id = cityId
        
    def json(self):
        return {
            'city_id': self.city_id, 
            'has_municipal_plan':self.has_municipal_plan, 
            'population_no_water': self.population_no_water, 
            'population_no_sewage': self.population_no_sewage, 
            'population_no_garbage_collection': self.population_no_garbage_collection
        }