from model.City import City
from configuration.config import ormDatabase

class CityService:
    def getCities(self):
        cities = City.query.all()
        return {"data": [{"id":city.id, "name": city.name, "state_id": city.state_id} for city in cities]}
    
    def saveCities(self, cities):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return {"data": [{'name': city.name} for city in cities], "status": True}