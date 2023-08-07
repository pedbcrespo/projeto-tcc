from flask_restful import Resource
from configuration.config import api
from service.StateService import StateService

baseUrl = '/states'

class Initial(Resource):
    def get(self):
        return {"message": "Funcionando"}

class StateController(Resource):
    service = StateService()

    def get(self):
        return self.service.getStates()

api.add_resource(Initial, "/")
api.add_resource(StateController, baseUrl)
