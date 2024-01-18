from rpaBase import driver, webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getAllCities, getStateById
import time

class RpaEmpresas:
    def __init__(self):
        self.xpath = {
            'button': '//*[@id="onetrust-accept-btn-handler"]',
            'iframe': '//*[@id="embedded-viz-wrapper"]/iframe',
            'iframeSpan': '//*[@id="tableauTabbedNavigation_tab_2"]',
            'MEISelect': '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_9"]/div/div[3]/span/div[1]',
            'MEIALLInput': '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_(All)"]/div[2]/input',
            'NOT_MEIInput': '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:opcao_mei:nk5201907744645360639_15609509314568364903_0"]/div[2]/input',
            'citySelect': '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5"]/div/div[3]/span/div[1]',
            'citySelectALL': '//*[@id="FI_federated.094r6uj0biqiya0zuf7q10pgukt8,none:nom_municipio:nk5201907744645360639_5969980573013623668_(All)"]/div[2]/input',
            'citySelectInput': '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5_textbox"]',
            'citySelectOptions': '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5_menu"]/div[2]',
            'downloadButton': '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/button[4]',
        }
        self.downloadButton = None 
        self.iframe = None

    def __selectInputCityName__(self, wait, cityName):
        citySelectInput = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5_textbox"]')))
        print("**ESCREVENDO")
        citySelectInput.send_keys(cityName)
        time.sleep(3)
        print("**PRESSIONANDO ENTER")
        citySelectInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def __getFirstOptionAfterSearch__(self):
        option = driver.find_element(By.CLASS_NAME, 'facetOverflow')
        tagInput = option.find_element(By.TAG_NAME, 'input')
        return tagInput
    

    def __getEnterprisesByCity__(self, wait, city):
        
        citySelectInput = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['citySelectInput'])))
        print("ESCREVENDO NOME DA CIDADE")
        self.__selectInputCityName__(wait, city['name'])
        print("BUSCANDO A PRIMEIRA OPCAO")
        self.__getFirstOptionAfterSearch__().click()
        time.sleep(3)
        print("PROCESSO DE DOWNLOAD")
        self.__downloadProcess__(city)
        time.sleep(2)
        wait = WebDriverWait(driver, 20)
        print("SELECIONANDO DENOVO O SELECT")
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_5"]/div/div[3]/span/div[1]'))).click()
        time.sleep(3)
        print("SELECIONANDO A CIDADE DENOVO PARA APAGAR")
        self.__selectInputCityName__(wait, city['name'])
        print("SELECIONANDO A PRIMEIRA OPCAO")
        self.__getFirstOptionAfterSearch__().click()
        print("LIMPANDO A BUSCA")
        citySelectInput.clear()

    def __getEnterprises__(self, wait):
        cities = getAllCities()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['citySelect']))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['citySelectALL']))).click()
        count = 1
        for city in cities[:5]:
            print(f"================================= {count}")
            self.__getEnterprisesByCity__(wait, city)
            count += 1
            print(f"=================================")
            time.sleep(2)


    def __downloadProcess__(self, city):
        state = getStateById(city['state_id'])
        driver.switch_to.default_content()
        waitLocal = WebDriverWait(driver, 20)
        self.downloadButton.click()
        time.sleep(2)

        downloadIframe = driver.find_element(By.XPATH, '//*[@id="embedded-viz-wrapper"]/iframe')
        driver.switch_to.frame(downloadIframe)

        button = driver.find_element(By.XPATH, '//*[@id="DownloadDialog-Dialog-Body-Id"]/div/fieldset/button[3]')
        button.click()
        time.sleep(2)

        csvOption = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[2]/div[2]/label[2]')))
        csvOption.click()
        time.sleep(2)


        driver.switch_to.default_content()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.HOME).perform()
        iframe = waitLocal.until(EC.presence_of_element_located((By.XPATH, self.xpath['iframe'])))
        driver.switch_to.frame(iframe)
        

    def __notMEIConfig__(self, wait):
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['MEISelect']))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['MEIALLInput']))).click()
        time.sleep(2)

        notMeiInput = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['NOT_MEIInput'])))
        notMeiInput.click()
        time.sleep(5)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
    def execute(self):
        driver.get('https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral')
        wait = WebDriverWait(driver, 20)
        try:
            button = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['button'])))
            button.click()
        except:
            pass
        self.downloadButton = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['downloadButton'])))
        self.iframe = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['iframe'])))
        driver.switch_to.frame(self.iframe)
        span = wait.until(EC.presence_of_element_located((By.XPATH, self.xpath['iframeSpan'])))
        span.click()

        self.__notMEIConfig__(wait)
        self.__getEnterprises__(wait)

if __name__ == '__main__':
    rpa = RpaEmpresas()
    rpa.execute()