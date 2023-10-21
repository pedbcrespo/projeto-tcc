from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity


states = getStates()

driver.get("https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral")
acceptCookiesId = 'onetrust-accept-btn-handler'
acceptCookiesButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, acceptCookiesId))
)
acceptCookiesButton.click()

divRoot = driver.find_element(By.ID, 'root')
divRootLv1 = divRoot.find_element(By.CLASS_NAME, '_app_919mw_1')
divRootLv2 = divRootLv1.find_elements(By.CLASS_NAME, '_content_919mw_7')
divRootLv3 = None
for i in range(10):
    try:
        divRootLv3 =  WebDriverWait(divRootLv2, 10).until(
            EC.presence_of_element_located(By.CLASS_NAME, '_container_16i18_1')
        )
    except:
        print('AINDA NAO ACHOU')

print(divRootLv3)


input('')
driver.close()