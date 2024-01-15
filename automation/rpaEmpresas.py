from rpaBase import driver, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity
import time

class RpaEmpresas:
    def __init__(self):
        self.xpath = {
            'button': '//*[@id="onetrust-accept-btn-handler"]',
            'iframe' : '//*[@id="embedded-viz-wrapper"]/iframe',
            'iframeSpan' : '//*[@id="tableauTabbedNavigation_tab_2"]',
            'MEISelect' : '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_9"]/div/div[3]/span/div[1]',
            'MEIALLInput' : '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_(All)"]/div[2]/input',
            'NOT_MEIInput' : '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_0"]/div[2]/input',
            'citySelect' : '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5"]/div/div[3]/span/div[1]',
            'citySelectALL' : '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:nom_municipio:nk5201907744645360639_5969980573013623668_(All)"]/div[2]/input'
        } 

    def __getEnterprises__(self, state, city):
        info = {}
        return info
    
    def execute(self):
        driver.get('https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral')
        wait = WebDriverWait(driver, 20)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['button'])))
            button.click()
        except:
            pass
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['iframe'])))
        driver.switch_to.frame(iframe)
        span = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['iframeSpan'])))
        span.click()

        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['MEISelect']))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['MEIALLInput']))).click()
        time.sleep(2)

        notMeiInput = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['NOT_MEIInput'])))
        notMeiInput.click()
        time.sleep(5)

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['citySelect']))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['citySelectALL']))).click()



if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()