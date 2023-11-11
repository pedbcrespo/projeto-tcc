from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from database import getStates, getStatesCity
from unidecode import unidecode
import functools as ft
import os

def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

class RpaSecurity:
    def __init__(self):
        self.url = 'https://app.powerbi.com/view?r=eyJrIjoiYjhhMDMxMTUtYjE3NC00ZjY5LWI5Y2EtZDljNzBlNDg2ZjVkIiwidCI6ImViMDkwNDIwLTQ0NGMtNDNmNy05MWYyLTRiOGRhNmJmZThlMSJ9'
        driver.get(self.url)
        try:
            self.wait = WebDriverWait(driver, 40)
            scroolBarContentXpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[4]'
            scroolBarDiv = self.wait.until(EC.presence_of_element_located((By.XPATH, scroolBarContentXpath)))
            scroolBar = scroolBarDiv.find_element(By.CSS_SELECTOR, '.scroll-bar-part-bar')
            xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]'
            div_table = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            presentationRowsXpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]/div[2]/div'
            presentationDiv = div_table.find_element(By.XPATH, presentationRowsXpath)
            self.securityInfo = []
            data = None 
            while data != ['Selecionar', 'Linha', 'TO', 'Xambioá', '4', '3', '2']:
                divs = presentationDiv.find_elements(By.CLASS_NAME, 'row')
                for div in divs:
                    data = div.text.split()
                    if data not in self.securityInfo:
                        self.securityInfo.append(data)
                clear()
                print('dados lidos:', len(self.securityInfo))
                self.rollDown(scroolBar)
        except:
            print('ERRO AO BUSCAR DADOS DO POWERBI')
        self.cleanInfo()
        self.fixValues()
        print('Dados coletados: ', len(self.securityInfo))
        
    def cleanInfo(self):
        self.securityInfo = list(map(lambda val: val[2:], self.securityInfo))
        
    def fixValues(self):
        def lastElement(arr):
            index = len(arr) -1
            return None if arr == [] else int(arr[index])
        def handleValues(val):
            names = list(filter(lambda x: not x.isnumeric(), val))
            numbers = list(filter(lambda x: x not in names, val))
            abbreviation = names.pop(0)
            return {'abbreviation': abbreviation, 'name': ''.join(names), 'rate': lastElement(numbers)}
        self.securityInfo = list(map(lambda val: handleValues(val), self.securityInfo))    
        
    def rollDown(self, scroolBar):
        actions = ActionChains(driver)
        actions.click_and_hold(scroolBar).move_by_offset(0, 2).release().perform()

    def createAvarage(self, state):
        abbreviation = state['abbreviation']
        stateList = list(filter(lambda val: val['abbreviation'] == abbreviation, self.securityInfo))
        rates = list(map(lambda val: val['rate'], stateList))
        ratesWithOutNone = list(filter(lambda val: val!=None, rates))
        sumRate = ft.reduce(lambda a,b: a+b, ratesWithOutNone)
        avg = round(sumRate/len(ratesWithOutNone), 2)
        return avg
        
    def execute(self, state, city):
        cityName = city['name']
        cityRate = list(filter(lambda data: data['name'] == cityName, self.securityInfo))
        return {'abbreviation': state['abbreviation'], 'name': cityName, 'rate': self.createAvarage(state)} if cityRate == [] else cityRate[0]

if __name__ == '__main__':
    rpa = RpaSecurity()
    states = getStates()
    for state in states:
        cities = getStatesCity(state['abbreviation'])
        for city in cities:
            print(city['name'])
