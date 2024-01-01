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
    
    def __moveDoubleClick__(self, x, y, timeWait=0):
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.click()
        time.sleep(timeWait)



    def execute(self):
        url = "https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral"
        currentMouseX, currentMouseY = pyautogui.position()
        print(f"{currentMouseX}, {currentMouseY}")
        # CLICA NO BRAVE
        self.__moveClickAndWait__(698, 1058)

        # CLICA NA BARRA DE URL
        self.__moveClickAndWait__(632, 58)

        # DIGITA O SITE E PRESSIONA ENTER
        pyautogui.write(url)
        pyautogui.press('enter')
        time.sleep(8)

        # CLICA NO "EMPRESAS POR ATIVIDADE..."
        self.__moveClickAndWait__(557, 319, 8)

        # CLICA NO SELECT DE MUNICIPIOS
        self.__moveClickAndWait__(60, 598, 1)

        # REMOVE OPCAO "TODOS"
        self.__moveClickAndWait__(37, 650, 3)
        
        # CLICA NO INPUT TEXTO DE BUSCA DE CIDADE
        self.__moveClickAndWait__(34, 622)

        for city in self.cities:
            # DIGITA NOME DA CIDADE
            pyautogui.write("")
            pyautogui.write(city['name'])
            time.sleep(3)

            # CLICA NO CHECKBOX RESULTADO
            self.__moveClickAndWait__(37, 650)
            
            # ESPERA ALGO
            time.sleep(5)

            # DESSELECIONA O CHECKBOX RESULTADO
            self.__moveClickAndWait__(37, 650, 5)

            # APAGA O NOME ESCRITO
            self.__moveClickAndWait__(264, 619, 2)

            # CLICA NO INPUT TEXTO DE BUSCA DE CIDADE
            self.__moveClickAndWait__(34, 622)


if __name__ == '__main__':
    rpa = rpaEmpresas2()
    rpa.execute()