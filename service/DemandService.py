from model.Demand import Demand
from model.City import City
from model.DemandLocation import DemandLocation
from request.DemandRequest import DemandRequest
from service.DistrictService import DistrictService
from configuration.config import ormDatabase

class DemandService:
    distirctService = DistrictService()
    
    def getAllDemands(self):
        demands = Demand.query.all()
        return [demand.json() for demand in demands]
    
    def getDemandOfCity(self, cityId:int):
        city = City.query.filter(City.id == cityId).first()
        districts = self.distirctService.getDistrictOfCity(city) 
        idDistricts = [district.id for district in districts]  
        demandsLocations = DemandLocation.query.filter(DemandLocation.district_id in idDistricts).all()
        demands = Demand.query.filter(Demand.id in [demand.demand_id for demand in demandsLocations]).all()
        return [demand.json() for demand in demands]
    
    def __save(self, model):
        ormDatabase.session.add(model)
        ormDatabase.session.commit()
    
    def saveDemand(self, demand:Demand):
        self.__save(demand)
        return demand.json()
    
    def saveLocationDemand(self, demandRequest:DemandRequest):
        demandLocation = demandRequest.getDemandLocation()
        self._save(demandLocation)
        return demandLocation.json()