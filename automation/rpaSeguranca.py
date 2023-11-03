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
    
    def getData(self):
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
            divs = presentationDiv.find_elements(By.CLASS_NAME, 'row')
            index = 0
            securityInfo = []
            while index < 5570:
                for div in divs:
                    if div.get_attribute('role') == 'row' and index == int(div.get_attribute('row-index')):
                        data = div.text.split()
                        print(data)
                        securityInfo.append(data)
                    index += 1
                self.rollDown(scroolBar)
            return securityInfo
        except:
            print('ERRO AO BUSCAR DADOS DO POWERBI')
        
        return []
        # driver.quit()


    def rollDown(self, scroolBar):
        actions = ActionChains(driver)
        actions.click_and_hold(scroolBar).move_by_offset(0, 500).release().perform()

    def execute(self, state, city):
        pass


rpa = RpaSecurity()

rpa.getData()