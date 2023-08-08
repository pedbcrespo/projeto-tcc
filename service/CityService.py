from model.City import City
from configuration import config

class CityService:
    def getCities(self):
        cities = City.query.all()
        return {"data": [{"id":city.id, "name": city.name} for city in cities]}