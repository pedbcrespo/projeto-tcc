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
        for city in cities[:1]:
            enterprises += self.__getEnterprises__(state, city)
        return enterprises

    def __getEnterprises__(self, state, city):
        info = {}

        xpathCloseAdd = '//*[@id="modal-base-backdrop"]/div/div/div/div/div[1]/img'
        xpathAcceptCookies = '/html/body/div[1]/div/a'
        # xpathLogInButton = '//*[@id="__nuxt"]/div/nav/div/div[5]/button'
        # xpathGoogleLoginButton = '//*[@id="container"]/div/div[2]'

        driver.get(self.getUrl(state, city))
        wait = WebDriverWait(driver, 10)
        
        closeButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathCloseAdd)))
        closeButton.click()
        
        acceptCookiesButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathAcceptCookies)))
        acceptCookiesButton.click()
        
        # loginButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathLogInButton)))
        # loginButton.click()

        # googleButton = wait.until(EC.presence_of_element_located((By.XPATH, xpathGoogleLoginButton)))
        # googleButton.click()

        xpathAmount = '//*[@id="__nuxt"]/div/div[1]/div[3]/div[1]/h1/span[1]'
        xpathTopEnterprisesTypes = '//*[@id="__nuxt"]/div/div[1]/div[3]/div[1]/div[3]/div[3]/div[1]'
        
        amountTag = wait.until(EC.presence_of_element_located((By.XPATH, xpathAmount)))
        info['amount'] = amountTag.text

        return []
    
    def execute(self):
        enterprises = []
        states = getStates()
        for state in states[:1]:
            enterprises += self.__getDataFromState__(state)

if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()