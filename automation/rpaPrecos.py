from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity, getState
from unidecode import unidecode
import functools as ft

class VivaReal:
    def __init__(self, abbreviation, cityName):
        self.abbreviation = abbreviation.lower()
        self.cityName = unidecode(cityName).lower().replace(' ','-')
        self.url = f"https://www.vivareal.com.br/venda/{self.abbreviation}/{self.cityName}"
    
    def process(self):
        driver.get(self.url)
        try:
            listPropertyCardValues = driver.find_elements(By.CLASS_NAME, 'property-card__values')
            print(listPropertyCardValues)
        except:
            print('-------FALHA------')
        return None

class ZapiMoveis:
    def __init__(self, abbreviation, cityName):
        self.abbreviation = abbreviation.lower()
        self.cityName = unidecode(cityName).lower().replace(' ','-')
        self.url = f"https://www.zapimoveis.com.br/venda/imoveis/{self.abbreviation}+{self.cityName}"
    
    
    def format(self, strNumber):
        number = int(strNumber.replace('R$','').replace('.',''))
        return number
    
    def process(self):
        print(self.url)
        prices = []
        try:
            driver.get(self.url)
            divsListingPrice = driver.find_elements(By.CLASS_NAME, 'listing-price')
            for elem in divsListingPrice:
                if 'R$' in elem.text:
                    if elem.text.count('R$') == 1:
                        prices.append(self.format(elem.text))
            avg = ft.reduce(lambda a,b: a+b, prices)/len(prices)
            print('-------SUCESSO------', avg)
            return ft.reduce(lambda a,b: a+b, prices)/len(prices)
        except:
            print('-------FALHA------')
        return prices

class ImovelWeb:
    def __init__(self, abbreviation, cityName):
        self.abbreviation = abbreviation.lower()
        self.cityName = unidecode(cityName).lower().replace(' ','-')
        self.url = f"https://www.imovelweb.com.br/imoveis-venda-{self.abbreviation}-{self.cityName}"

linksList = [VivaReal]
# linksList = [VivaReal, ZapiMoveis, ImovelWeb]


def link(state, city):
    sigla = state['abbreviation'].lower()
    name = unidecode(city['name']).lower().replace(' ','-')
    return f"{sigla}+{name}"

def getPrices(state, city):
    for link in linksList:
        site = link(state['abbreviation'], city['name'])
        try:
            return site.process()
        except:
            continue
    return None

def executa():
    # states = getStates()
    # for state in states:
    #     cities = getStatesCity(state['abbreviation'])
    #     prices = []
    #     for city in cities:
    #         prices.append(getPrices(state, city))
    state = getState('RJ')
    cities = getStatesCity(state['abbreviation'])
    getPrices(state, cities[0])
        
executa()