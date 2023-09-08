from configuration.config import ormDatabase

orm = ormDatabase

class DemandLocation(orm.Model):
    __tablename__ = 'demand_location'
    
    id = orm.Column(orm.Integer, primary_key=True)
    demand_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('demand.id'))
    district_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('district.id'))
    occurrence = ormDatabase.Column(ormDatabase.Integer)
    
    def __init__(self, demand_id, district_id):
        self.demand_id = demand_id
        self.district_id = district_id
        self.occurrence = 0
        
    def __repr__(self):
        return f"({self.id}, {self.demand_id}, {self.district_id})"
    
    def json(self):
        return {'id': self.id, 'demand_id': self.name}