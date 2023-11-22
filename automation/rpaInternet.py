from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from database import getStates, getStatesCity, getState
from unidecode import unidecode
import functools as ft
import time

class RpaInternet:
    def getUrl(self, linkName):
        return f'https://melhorplano.net/internet-banda-larga?l={linkName}'
    
    
    def __settingLinkName__(self, state, city):
        cityName = unidecode(city['name']).lower().replace(' ','%20')
        lowerAbbreviation = state['abbreviation'].lower()
        return f"{cityName}-{lowerAbbreviation}"
    
    def __getPrice__(self, div):
        spans = div.find_elements(By.TAG_NAME, 'span')
        spans = list(filter(lambda span: span.get_attribute('data-price') != None, spans))
        unit = ""
        decimal = ""
        for span in spans:
            if span.get_attribute('data-price') == 'unit':
                unit = span.text
            elif span.get_attribute('data-price') == 'decimal':
                decimal = span.text
        return float(f'{unit}{decimal}'.replace(',','.')) if unit != "" and decimal != "" else None
    
    def process(self, state, city):
        avgPrice = None
        print('buscando', state['abbreviation'], city['name'])
        print('puxando dados do site...')
        linkName = self.__settingLinkName__(state, city)
        driver.get(self.getUrl(linkName))
        wait = WebDriverWait(driver, 5)
        xpathListPrices = '//*[@id="comparison_scroll_id"]/div[2]/div[2]'
        listPrices = wait.until(EC.presence_of_element_located((By.XPATH, xpathListPrices)))
        divs = listPrices.find_elements(By.TAG_NAME, 'div')
        prices = list(map(lambda div: self.__getPrice__(div), divs))
        pricesWithoutNoneValues = list(filter(lambda price: price != None, prices))
        if pricesWithoutNoneValues == []:
            return None
        print('precos buscados')
        avgPrice = round(ft.reduce(lambda a,b: a+b, pricesWithoutNoneValues)/len(pricesWithoutNoneValues) ,2)
        driver.delete_all_cookies()
        return avgPrice
    
    def execute(self, state, city):
        return self.process(state, city)
    
    
if __name__ == '__main__':
    rpa = RpaInternet()
    states = getStates()
    for state in states:
        cities = getStatesCity(state['abbreviation'])
        for city in cities:
            time.sleep(5)
            print(city['name'], rpa.execute(state, city))