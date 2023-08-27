from model.District import District 
from model.City import City 
from typing import List
from configuration.config import ormDatabase


class DistrictService:
    def getDistricts(self):
        districts =  District.query.all()
        return districts
       
    def getDistrictOfCity(self, city:City):
        districts = District.query.filter(District.city_id==city.id).all()
        return districts
        
    def saveDistricts(self, districts:List[District]):
        ormDatabase.session.add_all(districts)
        ormDatabase.session.commit()
        return districts