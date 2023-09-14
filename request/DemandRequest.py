from model.DemandLocation import DemandLocation

class DemandRequest:
    def __init__(self, demand, district):
        self.demand = demand
        self.district = district
        
    def getDemandLocation(self):
        return DemandLocation(self.demand.id, self.district.id)