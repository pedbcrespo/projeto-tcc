from rpaBase import driver, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getAllCities, getStates, getStatesCity, getStateById
from unidecode import unidecode
import time

class RpaCoustLiving:
    def formatName(self, name):
        nameWithoutAccents = unidecode(name)
        formatedName = nameWithoutAccents.lower().replace(' ', '-')
        return formatedName

    def __getUrl__(self, state, city):
        stateLowerCase = state['abbreviation'].lower()
        cityFormated = self.formatName(city['name'])
        return f"http://www.custodevida.com.br/{stateLowerCase}/{cityFormated}/"
    
    def __getValuesFromTable__(self, table):
        valueList = []
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            textValues = row.text.split('R$')
            valueList.append({
                textValues[0]: float(textValues[1].replace('.', '').replace(',', '.'))
            })
        return valueList
            

    def __getInfoCity__(self, state, city):
        url = self.__getUrl__(state, city)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        section = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
        tables = section.find_elements(By.TAG_NAME, 'table')
        valuesList = []
        for table in tables:
            valuesList += self.__getValuesFromTable__(table)
        return valuesList
    
    def execute(self):
        states = getStates()
        cities = getStatesCity(states[0]['abbreviation'])
        valuesList = []
        for state in states[:3]:
            cities = getStatesCity(state['abbreviation'])
            for city in cities[:5]:
                try:
                    valuesList += self.__getInfoCity__(state, city)
                except:
                    print(state['abbreviation'], city['name'], 'Dados nao econtrados')
if __name__ == '__main__':
    rpa = RpaCoustLiving()
    rpa.execute()