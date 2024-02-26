import unidecode
from rpaBase import driver, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getAllCities, getStates, getStatesCity, getStateById, saveEnterprises

class RpaTopSectionsEnterprises:
    def getUrl(self, state, city):
        stateAbbreviation = state['abbreviation']
        cityName = city['name'].replace(' ', '-')
        location = unidecode.unidecode(f"{stateAbbreviation}-{cityName}").lower()
        return f"https://www.econodata.com.br/empresas/{location}"

    def getTopSectionsEnterprise(self, wait):
        pass

    def execute(self):
        for state in getStates():
            for city in getStatesCity(state['abbreviation']):
                url = self.getUrl(state, city)
                driver.get(url)
                self.getTopSectionsEnterprise(WebDriverWait(driver, 10))
                