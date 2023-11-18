from rpaBase import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity, getState
from unidecode import unidecode
import functools as ft
import time

class Site:
    def handlePrices(self, textPrice):
        splitedTextPrice = textPrice.replace('R$','').split('.')
        lastNumber = splitedTextPrice[-1]
        number = ''.join(splitedTextPrice[:-1])
        if len(lastNumber) == 2:
            number += '.' + splitedTextPrice[-1] 
        else:
            number += splitedTextPrice[-1]
        return float(number)

class VivaReal(Site):
    def __init__(self, abbreviation, cityName):
        self.abbreviation = abbreviation.lower()
        self.cityName = unidecode(cityName).lower().replace(' ','-')
        self.url = f"https://www.vivareal.com.br/venda/{self.abbreviation}/{self.cityName}"
    
    def process(self):
        print(self.url)
        driver.get(self.url)
        prices = []
        avg = None
        try:
            listPropertyCardValues = driver.find_elements(By.CLASS_NAME, 'property-card__values')
            for select in listPropertyCardValues:
                if select.text.count('R$') == 1:
                    prices.append(self.handlePrices(select.text))
            avg = round(ft.reduce(lambda a,b: a+b, prices)/len(prices), 2)
            print('-------SUCESSO------', avg)
        except:
            print('-------FALHA------', avg)
        return avg
            
class ZapiMoveis(Site):
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
        avg = None
        try:
            driver.get(self.url)
            divsListingPrice = driver.find_elements(By.CLASS_NAME, 'listing-price')
            for elem in divsListingPrice:
                if elem.text.count('R$') == 1:
                    prices.append(self.handlePrices(elem.text))
            avg = round(ft.reduce(lambda a,b: a+b, prices)/len(prices), 2)
            print('-------SUCESSO------', avg)
        except:
            print('-------FALHA------', avg)
        return avg

        
class ImovelWeb(Site):
    def __init__(self, abbreviation, cityName):
        self.abbreviation = abbreviation.lower()
        self.cityName = unidecode(cityName).lower().replace(' ','-')
        self.url = f"https://www.imovelweb.com.br/imoveis-venda-{self.abbreviation}-{self.cityName}"


def link(state, city):
    sigla = state['abbreviation'].lower()
    name = unidecode(city['name']).lower().replace(' ','-')
    return f"{sigla}+{name}"

def getPrices(sites, state, city):
    resultado = None
    for link in sites:
        time.sleep(3)
        site = link(state['abbreviation'], city['name'])
        resultado = site.process()
        if resultado != None:
            break
    return resultado

class RpaPrices:
    def __init__(self):
        self.linksList = [VivaReal, ZapiMoveis]
        print('RPA Precos iniciado')
        
    def execute(self, state, city):
        return getPrices(self.linksList, state, city)

if __name__ == '__main__':
    state = getState('RJ')
    cities = getStatesCity(state['abbreviation'])   
    rpa = RpaPrices()  
    for city in cities:
        rpa.execute(state, city)  