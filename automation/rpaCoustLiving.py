from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getAllCities, getStates, getStatesCity, getStateById
from unidecode import unidecode
import time
import os

class RpaCoustLiving:
    def formatName(self, name):
        nameWithoutAccents = unidecode(name)
        formatedName = nameWithoutAccents.lower().replace(' ', '-')
        return formatedName

    def __getUrl__(self, state, city):
        stateLowerCase = state['abbreviation'].lower()
        cityFormated = self.formatName(city['name'])
        return f"http://www.custodevida.com.br/{stateLowerCase}/{cityFormated}/"
    
    def readTxtFile(self, currentFile='readedCities.txt'):
        try:
            with open(currentFile, 'r') as arquivo:
                cities = arquivo.read().splitlines()
                print(f'Lista de palavras no arquivo "{currentFile}": {cities}')
                return cities

        except IOError as e:
            print(f"Erro ao tentar abrir o arquivo {currentFile}: {e}")
            return None

    def __writeOnTxtFile__(self, fileName, name):
        try:
            with open(fileName, 'a+', encoding='utf-8') as file:
                file.seek(0, 2)
                file.write(f"{name}\n")

        except IOError as e:
            print(f"Erro ao tentar abrir o file {fileName}: {e}")

    def __getCities__(self, state):
        citiesRead = self.readTxtFile()
        cities = getStatesCity(state['abbreviation'])
        filtredCities = [city for city in cities if city['name'] not in citiesRead]
        return filtredCities

    def __getStates__(self):
        statesRead = self.readTxtFile('readedStates.txt')
        states = getStates()
        filtredStates = [state for state in states if state['name'] not in statesRead]
        return filtredStates


    def __getValuesFromTable__(self, wait, table):
        valueList = []
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            textValues = row.text.split('R$')
            valueList.append({
                textValues[0]: float(textValues[1].replace('.', '').replace(',', '.'))
            })
        return valueList
            
    def __getInfoCity__(self, driver):
        wait = WebDriverWait(driver, 10)
        section = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
        tables = section.find_elements(By.TAG_NAME, 'table')
        valuesList = []
        for table in tables:
            valuesList += self.__getValuesFromTable__(wait, table)
        print(valuesList)
        return valuesList
    
    def execute(self):
        valuesList = []
        for state in self.__getStates__():
            for city in self.__getCities__(state):
                print('==============================')
                print(state['abbreviation'], city['name'])
                try:
                    url = self.__getUrl__(state, city)
                    driver.get(url)
                    valuesList += self.__getInfoCity__(state)
                except:
                    print('========== Dados nao econtrados ==========')
                finally:
                    self.__writeOnTxtFile__('./readedCities.txt', city['name'])
            self.__writeOnTxtFile__('./readedStates.txt', state['name'])
if __name__ == '__main__':
    rpa = RpaCoustLiving()
    rpa.execute()