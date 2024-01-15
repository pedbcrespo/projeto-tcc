from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
import time

class RpaEmpresas:
    def __getEnterprises__(self, state, city):
        info = {}
        return info
    
    def execute(self):
        xpathButton = '//*[@id="onetrust-accept-btn-handler"]'
        xpathIframe = '//*[@id="embedded-viz-wrapper"]/iframe'
        xpathIframContent = '//*[@id="centeringContainer"]'

        driver.get('https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral')
        wait = WebDriverWait(driver, 20)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, xpathButton)))
            button.click()
        except:
            pass
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, xpathIframe)))
        driver.switch_to.frame(iframe)
        content = wait.until(EC.presence_of_element_located((By.XPATH, xpathIframContent)))
        print(content)

if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()