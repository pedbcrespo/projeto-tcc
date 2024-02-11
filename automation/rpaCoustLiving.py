from rpaBase import driver, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getAllCities, getStates, getStatesCity, getStateById
from unidecode import unidecode
class RpaCoustLiving:

    def formatName(name):
        nameWithoutAccents = unidecode(name)
        formatedName = nameWithoutAccents.lower().replace(' ', '-')
        return formatedName

    def __getUrl__(self, state, city):
        stateLowerCase = state['abbreviation'].lower()
        cityFormated = self.formatName(city['name'])
        return f"http://www.custodevida.com.br/{stateLowerCase}/{cityFormated}/"
    
    def execute(self):
        states = getStates()
        for state in states:
            cities = getStatesCity(state['abbreviation'])
            for city in cities:
                driver.get(self.__getUrl__(state, city))

if __name__ == '__main__':
    rpa = RpaCoustLiving()
    rpa.execute()