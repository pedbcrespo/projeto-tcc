from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from database import getStates, getStatesCity
from unidecode import unidecode

class RpaSecurity:
    def __init__(self):
        self.url = 'https://app.powerbi.com/view?r=eyJrIjoiYjhhMDMxMTUtYjE3NC00ZjY5LWI5Y2EtZDljNzBlNDg2ZjVkIiwidCI6ImViMDkwNDIwLTQ0NGMtNDNmNy05MWYyLTRiOGRhNmJmZThlMSJ9'
        driver.get(self.url)
        try:
            self.wait = WebDriverWait(driver, 40)
            scroolBarContentXpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[4]'
            scroolBarDiv = self.wait.until(EC.presence_of_element_located((By.XPATH, scroolBarContentXpath)))
            scroolBar = scroolBarDiv.find_element(By.CSS_SELECTOR, '.scroll-bar-part-bar')
            xpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]'
            div_table = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            presentationRowsXpath = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[11]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div[1]/div[2]/div'
            presentationDiv = div_table.find_element(By.XPATH, presentationRowsXpath)
            index = 0
            self.securityInfo = []
            data = None 
            while data != ['Selecionar', 'Linha', 'TO', 'Xambioá', '4', '3', '2']:
                divs = presentationDiv.find_elements(By.CLASS_NAME, 'row')
                for div in divs:
                    data = div.text.split()
                    print(data)
                    if data not in self.securityInfo:
                        self.securityInfo.append(data)
                    index += 1
                if index == 5570:
                    break
                self.rollDown(scroolBar)
            print('Dados coletados: ', len(self.securityInfo))
        except:
            print('ERRO AO BUSCAR DADOS DO POWERBI')
        self.cleanInfo()
        print(self.securityInfo[0])
        
    def cleanInfo(self):
        self.securityInfo = list(map(lambda val: val[2:], self.securityInfo))
        
        
    def rollDown(self, scroolBar):
        actions = ActionChains(driver)
        actions.click_and_hold(scroolBar).move_by_offset(0, 2).release().perform()

    def execute(self, state, city):
        pass


rpa = RpaSecurity()
