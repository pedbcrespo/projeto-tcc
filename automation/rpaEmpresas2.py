from rpaBase import driver, webdriver
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
        xpathIframeSpan = '//*[@id="tableauTabbedNavigation_tab_2"]'
        xpathMEISelect = '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_9"]/div/div[3]/span/div[1]'
        xpathALLInput = '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_(All)"]/div[2]/input'
        xpathNOT_MEIInput = '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_0"]/div[2]/input'
        xpathCitySelect = '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5"]/div/div[3]/span/div[1]'
        xpathCitySelectALL = '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:nom_municipio:nk5201907744645360639_5969980573013623668_(All)"]/div[2]/input'


        driver.get('https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral')
        wait = WebDriverWait(driver, 20)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, xpathButton)))
            button.click()
        except:
            pass
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, xpathIframe)))
        driver.switch_to.frame(iframe)
        span = wait.until(EC.presence_of_element_located((By.XPATH, xpathIframeSpan)))
        span.click()

        wait.until(EC.presence_of_element_located((By.XPATH, xpathMEISelect))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, xpathALLInput))).click()
        time.sleep(2)

        notMeiInput = wait.until(EC.presence_of_element_located((By.XPATH, xpathNOT_MEIInput)))
        notMeiInput.click()
        time.sleep(5)

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        wait.until(EC.presence_of_element_located((By.XPATH, xpathCitySelect))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, xpathCitySelectALL))).click()



if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()