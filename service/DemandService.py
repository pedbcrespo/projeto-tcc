from model.Demand import Demand
from model.DemandLocation import DemandLocation
from configuration.config import ormDatabase

class DemandService:
    def getAllDemands(self):
        demands = Demand.query.all()
        return [demand.json() for demand in demands]
    
    def getDemandOfCity(self, cityId):
        None