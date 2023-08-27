from flask import Flask
from configuration.config import app
from controller.StateController import StateController
from controller.CityController import *
from controller.ExternApiController import *

if __name__ == '__main__':
    app.run()