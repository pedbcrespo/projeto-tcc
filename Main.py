from flask import Flask
from configuration.config import app
from controller.StateController import StateController

if __name__ == '__main__':
    app.run()
