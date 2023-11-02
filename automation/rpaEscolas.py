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
        
    def execute(self, state, city):
        cityName = city['name']
        stateLink = self.link(state)
        try:
            driver.get(f"https://qedu.org.br/uf/{stateLink}/busca")
            sections = driver.find_elements(By.XPATH, "//section[not(@*)]")
            for section in sections:
                divs = section.find_elements(By.XPATH, "//div[@class='flex flex-col font-bold']")
                for div in divs:
                    h1 = div.find_element(By.TAG_NAME, 'h1')
                    if h1.text == cityName:
                        p = div.find_element(By.TAG_NAME, 'p')
                        amount = self.handleNumberText(p.text)
                        print(state['abbreviation'], city['name'], amount, 'Escolas' if amount>1 else 'Escola')
                        return amount
        except:
            print(f"ERRO AO BUSCAR QTD ESCOLAS {state['abbreviation']} - {city['name']}")
        return None
    
rpa = RpaSchools()
states = getStates()
for state in states:
    cities = getStatesCity(state['abbreviation'])
    for city in cities:
        rpa.execute(state, city)
