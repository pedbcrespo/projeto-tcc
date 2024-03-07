from flask_restful import Resource
from flask import redirect, request
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.InfoService import InfoService


class Questions(Resource):
    def get(self):
        infoService = InfoService()
        return infoService.getQuestions()
    
api.add_resource(Questions, f"{BASE_URL}/questions")