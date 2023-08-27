from flask_restful import Resource
from configuration.config import api
from service.IbgeService import IbgeService

baseUrl = '/ibge-data'
class IbgeController(Resource):
    service = IbgeService()
    def get(self):
        return self.service.settingData()
    
api.add_resource(IbgeController, f"{baseUrl}")