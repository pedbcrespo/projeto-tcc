from flask import Flask
from configuration.config import app
from controller.StateController import StateController
from controller.CityController import CityController
from controller.IbgeController import IbgeController

if __name__ == '__main__':
    app.run()