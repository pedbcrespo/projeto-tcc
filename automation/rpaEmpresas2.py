import pyautogui
from database import getAllCities

class rpaEmpresas2:
    def __init__(self):
        self.cities = getAllCities()

    