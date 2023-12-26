from rpaBase import driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import getStates, getStatesCity


states = getStates()

driver.get("https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral")
acceptCookiesId = 'onetrust-accept-btn-handler'

wait = WebDriverWait(driver, 20)
acceptCookiesButton = wait.until(
        EC.presence_of_element_located((By.ID, acceptCookiesId))
)
acceptCookiesButton.click()
div1class = '_content_919mw_7'
div2class = '_container_16i18_1'

div = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'div2class'))
)

print(div)

# divRoot = driver.find_element(By.ID, 'root')


input('')
driver.close()