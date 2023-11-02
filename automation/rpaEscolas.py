from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
from unidecode import unidecode
import pandas as pd

class RpaSchools:
    def __init__(self):
        print('RPA Escolas iniciado')
        
    def link(self, state):
        name = unidecode(state['name']).lower().replace(' ','-')
        return f"{state['ibge_id']}-{name}"

    def handleNumberText(self, text):
        listText = text.split()
        numbers = list(filter(lambda val: val.isnumeric() ,listText))
        if numbers == []:
            return 0
        return int(numbers[0])
    
    def gettingCityDiv(self, section, cityName):
        divs = section.find_elements(By.TAG_NAME, 'div')
        for div in divs:
            if div.get_attribute('class') != 'flex flex-col font-bold':
                continue
            h1 = div.find_element(By.TAG_NAME, 'h1')
            if h1.text != cityName:
                return True
        return False

    def executa(self, state, city):
        cityName = city['name']
        stateLink = self.link(state)
        try:
            driver.get(f"https://qedu.org.br/uf/{stateLink}/busca")
            sections = [section for section in driver.find_elements(By.TAG_NAME, 'section')]
            filteredSections = list(filter(lambda section: self.gettingCityDiv(section, cityName), sections))
            if filteredSections == []:
                return None
            section = filteredSections[0]
            divs = [div for div in section.find_elements(By.TAG_NAME, 'div')]
            filtredDiv = list(filter(lambda div: div.get_attribute('class') == 'flex flex-col font-bold', divs))
            div = filtredDiv[0]
            p = div.find_element(By.TAG_NAME, 'p')
            amount = self.handleNumberText(p.text)
            print(state['abbreviation'], city['name'], amount, 'Escolas')
            return amount 
        except:
            print(f"ERRO AO BUSCAR QTD ESCOLAS {state['abbreviation']} - {city['name']}")
        return None
    
rpa = RpaSchools()
states = getStates()
for state in states:
    cities = getStatesCity(state['abbreviation'])
    for city in cities:
        rpa.executa(state, city)