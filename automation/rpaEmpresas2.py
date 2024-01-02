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


    def accessSite(self):
        url = "https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral"
        # CLICA NO BRAVE
        self.__moveClickAndWait__(698, 1058)

        # CLICA NA BARRA DE URL
        self.__moveClickAndWait__(632, 58)

        # DIGITA O SITE E PRESSIONA ENTER
        pyautogui.write(url)
        pyautogui.press('enter')
        time.sleep(8)

    def prepareToSearch(self):
        # CLICA NO "EMPRESAS POR ATIVIDADE..."
        self.__moveClickAndWait__(557, 319, 8)

        # CLICA NO SELECT DE MUNICIPIOS
        self.__moveClickAndWait__(60, 598, 1)

        # REMOVE OPCAO "TODOS"
        self.__moveClickAndWait__(37, 650, 3)
        
        # CLICA NO INPUT TEXTO DE BUSCA DE CIDADE
        self.__moveClickAndWait__(34, 622)

    def processToDownload(self, cityName):
        # CLICA NO BOTAO DE BAIXAR
        self.__moveClickAndWait__(1739, 273, 3)
        # CLICA NA OPCAO DE BAIXAR DADOS DE TABELA CRUZADOS
        self.__moveClickAndWait__(937, 717, 1)
        # SELECIONA A OPCAO CSV
        self.__moveClickAndWait__(805, 339)

        # CLICA NA OPCAO BAIXAR
        self.__moveClickAndWait__(1144, 383, 3)

        # CLILCA NO PATH AONDE SALVARA O ARQUIVO
        # self.__moveClickAndWait__(466, 51, 1)
        # pyautogui.write("C:\\Users\\User\\Documents\\Programacao\\projeto-tcc\\csvData\\enterprises")
        # pyautogui.press('enter')

        # CLICA NO CAMPO TEXTO PARA SALVAR O ARQUIVO
        self.__moveClickAndWait__(405, 465)

        # APERTA SEQUENCIA DE TECLAS PARA SELECIONAR TODO O TEXTO E ESCREVER O NOME DO ARQUIVO
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(f"{cityName}-empresas")
        pyautogui.press('enter')
        pyautogui.press('home')
        time.sleep(3)

    def preparationToNewSearch(self, cityName):
        # CLICA NO SELECT DE MUNICIPIOS
        self.__moveClickAndWait__(40, 594, 1)

        # ESCREVE O NOME DA CIDADE DENOVO    
        pyautogui.write(cityName)
        time.sleep(2)

        # CLICA NO RESULTADO
        self.__moveClickAndWait__(37, 647, 3)

        # APAGA O NOME
        self.__moveClickAndWait__(267, 620)

        # CLICA NO INPUT TEXTO DO NOME
        self.__moveClickAndWait__(45, 623)

    def execute(self):
        currentMouseX, currentMouseY = pyautogui.position()
        print(f"{currentMouseX}, {currentMouseY}")
        self.accessSite()
        self.prepareToSearch()

        for city in self.cities:
            # DIGITA NOME DA CIDADE
            pyautogui.write("")
            pyautogui.write(city['name'])
            time.sleep(3)

            # CLICA NO CHECKBOX RESULTADO
            self.__moveClickAndWait__(37, 650, 5)

            self.processToDownload(city['name'])
            self.preparationToNewSearch(city['name'])
        
        
        
                
if __name__ == '__main__':
    rpa = rpaEmpresas2()
    rpa.execute()