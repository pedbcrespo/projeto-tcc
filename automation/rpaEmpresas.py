from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
from unidecode import unidecode

class RpaEmpresas:
    def getUrl(self, state, city):
        abbreviation = (state['abbreviation']).lower()
        cityName = unidecode(city['name']).lower().replace(' ','-')
        return f"https://www.econodata.com.br/empresas/{abbreviation}-{cityName}"
    
    def execute(self):
        pass

if __name__ == '__main__':
    pass