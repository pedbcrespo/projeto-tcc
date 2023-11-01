from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity, getState
import functools as ft

class CitySecurityRate:
    def __init__(self, abbreviation, cityName, rate):
        self.abbreviation = abbreviation
        self.cityName = cityName
        self.rate = rate
        
    def __str__(self):
        return f'({self.abbreviation}, {self.cityName}, {self.rate})'

class RpaSecurity:
    def __init__(self):
        self.citySecurityData = []
        url = 'https://infograficos.gazetadopovo.com.br/seguranca-publica/atlas-da-violencia-2019-por-municipios/'
        driver.get(url)
        table_tag = driver.find_element(By.TAG_NAME, 'tbody')
        t_rows = table_tag.find_elements(By.TAG_NAME, 'tr')
        abbreviation=''
        cityName = ''
        rate = ''
        for row in t_rows:
            tds = row.find_elements(By.TAG_NAME, 'td')
            for td in tds:
                if td.get_attribute('class') == 'uf footable-visible footable-first-column':
                    abbreviation = td.text
                elif td.get_attribute('class') == 'municipio footable-visible':
                    cityName = td.text
                elif td.get_attribute('class') == 'taxa-estimada-de-homicidios footable-visible':
                    rate = float(td.text.replace(',','.'))
            self.citySecurityData.append(CitySecurityRate(abbreviation, cityName, rate))
        print('RPA Seguranca iniciado')
        
    def calculatingAvarageRate(self, abbreviation, cityName):
        cities = list(filter(lambda city: city.abbreviation == abbreviation, self.citySecurityData))
        rates = list(map(lambda city: city.rate, cities))
        avarageRate = round(ft.reduce(lambda a, b: a + b, rates)/len(cities), 2)
        return avarageRate

    def executa(self, state, city):
        abbreviation = state['abbreviation']
        cityName = city['name']
        data = list(filter(lambda dt: dt.cityName == cityName, self.citySecurityData))
        rate = self.calculatingAvarageRate(abbreviation, cityName)
        return rate if data == [] else data[0].rate


state = getState('RJ')
cities = getStatesCity(state['abbreviation'])  
rpa = RpaSecurity()
print(f'MEDIA {cities[0]["name"]}', rpa.executa(state, cities[0]))