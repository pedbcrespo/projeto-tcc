from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
import time

class RpaEmpresas:
    def getUrl(self, state, city):
        abbreviation = (state['abbreviation']).lower()
        cityName = city['name'].lower().replace(' ','-')
        return f"https://www.econodata.com.br/empresas/{abbreviation}-{cityName}"

    def __getDataFromState__(self, state):
        enterprises = []
        abbreviation = state['abbreviation']
        cities = getStatesCity(abbreviation)
        for city in cities:
            enterprises.append(self.__getEnterprises__(state, city))
        return enterprises

    def __getEnterprises__(self, state, city):
        info = {}

        xpathAmount = '//*[@id="__nuxt"]/div/div[1]/div[3]/div[1]/h1/span[1]'
        xpathEnterprisesTypeListButton = '//*[@id="__nuxt"]/div/div[1]/div[3]/div[1]/div[3]/div[3]/div[3]/div[2]/span[2]'
        xpathTypesTable = '//*[@id="empresas-abertas-recentemente-section"]/div[2]/div[2]/div/div[1]/table/tbody'

        driver.get(self.getUrl(state, city))
        wait = WebDriverWait(driver, 10)
        amountTag = wait.until(EC.presence_of_element_located((By.XPATH, xpathAmount)))
        typeListButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathEnterprisesTypeListButton)))
        typeListButton.click()
        typeTable = wait.until(EC.presence_of_element_located((By.XPATH, xpathTypesTable)))
        info['amount'] = int(amountTag.text.replace('.', ''))
        print(info['amount'], typeTable) 
        return info
    
    def execute(self):

        xpathCloseAdd = '//*[@id="modal-base-backdrop"]/div/div/div/div/div[1]/img'
        xpathAcceptCookies = '/html/body/div[1]/div/a'

        driver.get('https://www.econodata.com.br/empresas/')
        wait = WebDriverWait(driver, 20)
        
        closeButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathCloseAdd)))
        closeButton.click()
        
        acceptCookiesButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathAcceptCookies)))
        acceptCookiesButton.click()

        enterprises = []
        states = getStates()
        for state in states[:1]:
            enterprises += self.__getDataFromState__(state)

if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()