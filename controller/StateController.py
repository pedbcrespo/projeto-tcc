from flask_restful import Resource
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.StateService import StateService

class Initial(Resource):
    def get(self):
        return {"message": "Funcionando"}

class StateController(Resource):
    service = StateService()

    def get(self):
        return self.service.getStates()

api.add_resource(Initial, "/teste")
api.add_resource(StateController, f"{BASE_URL}/states")
