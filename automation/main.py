import database as db
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from csvGeneralCity import CsvGeneralCity
import os

def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def schoolsInformations(state, city, general_info):
    print("COLETANDO DADOS DE ESCOLARIDADE")
    rpaSchools = RpaSchools()
    scholarityRate = general_info['escolaridade']
    amountSchools = rpaSchools.executa(state, city)
    try:
        db.saveSchoolsInfo(city, amountSchools, scholarityRate)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")
    
def pricesInformation(state, city, general_info):
    print("COLETANDO DADOS DOS PRECOS")
    rpaPrices = RpaPrices()
    avgHomePrices = rpaPrices.executa(state, city)
    try:
        db.savePricesInfo(city, avgHomePrices)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")

def securityInformation(state, city):
    print("COLETANDO DADOS DA SEGURANCA")
    rpaSecurity = RpaSecurity()
    securityRate = rpaSecurity.executa(state, city)
    try:
        db.saveSecurityInfo(city, securityRate)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")

def generalInformation(state, city):
    print("COLETANDO DADOS GERAIS")
    generalCsv = CsvGeneralCity()
    generalInfo = generalCsv.execute(state, city)
    try:
        db.saveGeneralInfo(city, generalInfo)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")
    return generalInfo

def execute():
    print("EXECUTANDO RPA")
    states = db.getStates()
    for state in states:    
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(state['abbreviation'], city['name'])
            general_info = generalInformation(state, city)
            # if general_info == None:
            #     return None
            # schoolsInformations(state, city, general_info)
            # pricesInformation(state, city, general_info)
            # securityInformation(state, city)
execute()


