import pyautogui
from database import getAllCities
import time

class rpaEmpresas2:
    def __init__(self):
        self.cities = getAllCities()

    def __moveClickAndWait__(self, x, y, timeWait=0):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(timeWait)

    def __unSelect__(self):
        self.__moveClickAndWait__(37, 649, 1)
        self.__moveClickAndWait__(268, 621)


    def execute(self):
        url = "https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral"
        currentMouseX, currentMouseY = pyautogui.position()
        print(currentMouseX, currentMouseY)
        # CLICA NO BRAVE
        self.__moveClickAndWait__(698, 1058)

        # CLICA NA BARRA DE URL
        self.__moveClickAndWait__(632, 58)

        # DIGITA O SITE E PRESSIONA ENTER
        pyautogui.write(url)
        pyautogui.press('enter')
        time.sleep(8)

        # CLICA NO "EMPRESAS POR ATIVIDADE..."
        self.__moveClickAndWait__(557, 319, 10)

        # CLICA NO SELECT DE MUNICIPIOS
        self.__moveClickAndWait__(60, 598, 1)
            



if __name__ == '__main__':
    rpa = rpaEmpresas2()
    rpa.execute()