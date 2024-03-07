from flask import Flask
from configuration.config import app
from controller.StateController import *
from controller.CityController import *
from controller.QuestionController import *

startApp = app

if __name__ == '__main__':
    startApp.run()