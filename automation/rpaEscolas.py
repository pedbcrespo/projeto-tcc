from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
from unidecode import unidecode
import pandas as pd

class RpaSchools:
    def __init__(self):
        self.citySchoolsAmount = {}
        
    def link(self, state):
        name = unidecode(state['name']).lower().replace(' ','-')
        return f"{state['ibge_id']}-{name}"

    def executa(self, state, cityName):
        stateLink = self.link(state)
        driver.get(f"https://qedu.org.br/uf/{stateLink}/busca")
        sections = driver.find_elements(By.TAG_NAME, 'section')
        for section in sections:
            try:
                h1 = section.find_element(By.TAG_NAME, 'h1')
                if h1.get_attribute("x-text") != 'item.nome':
                    continue
                p = section.find_element(By.CLASS_NAME, 'text-xs')
                if ('escola' in p.text or 'escolas' in p.text) and len(p.text) <= 15:
                    text = p.text.replace('escolas', '')
                    amount = int(text)
                    cityName = h1.text
                    self.citySchoolsAmount[cityName] = amount 
            except:
                pass 
        return self.citySchoolsAmount[cityName]