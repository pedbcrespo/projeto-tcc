from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
from unidecode import unidecode

class RpaHospitals:
    def __init__(self):
        self.baseUrl = 'https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=ACRE'
        driver.get(self.baseUrl)
        self.forms = driver.find_elements(By.TAG_NAME, 'form')
        self.selects = driver.find_elements(By.TAG_NAME, 'select')
        
    def setUrl(self, stateCode, cityName):
        searchedName = cityName.upper().replace(' ', f'%{stateCode}')
        url = f'https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search={searchedName}'
        return url
    
    def getAmountHospitals(self, stateName, cityName):
        pass
        
        