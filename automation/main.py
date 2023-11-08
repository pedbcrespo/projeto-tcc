import database as db
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from csvGeneralCity import CsvGeneralCity
import threading
import os


def schoolsInformations(states):
    infos = []
    rpaSchools = RpaSchools()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS DE ESCOLARIDADE :: {state['abbreviation']} :: {city['name']}")
            amount = rpaSchools.execute(state, city)
            rate = generalInformation(state, city)['escolaridade']
            data = {'city':city, 'amount': amount, 'rate': rate}
            print(f"ESCOLAS {city['name']}:{data['amount']}")
            infos.append(data)
    try:
        db.saveSchoolsInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except Exception as e:
        print("ERRO AO SALVAR", str(e))
    
def pricesInformations(states):
    infos = []
    rpaPrices = RpaPrices()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS DOS PRECOS :: {state['abbreviation']} :: {city['name']}")
            avgHomePrices = rpaPrices.execute(state, city)
            infos.append({'city': city, 'price': avgHomePrices})
    try:
        db.savePricesInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")

def securityInformations(states):
    infos = []
    rpaSecurity = RpaSecurity()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS SEGURANCA :: {state['abbreviation']} :: {city['name']}")
            securityRate = rpaSecurity.execute(state, city)
            infos.append({'city':city, 'rate': securityRate})
    try:
        db.saveSecurityInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")

def generalInformation(state, city):
    generalCsv = CsvGeneralCity()
    generalInfo = generalCsv.execute(state, city)
    # try:
    #     db.saveGeneralInfo(city, generalInfo)
    #     print("DADOS SALVOS COM SUCESSO")
    # except:
    #     print("ERRO AO SALVAR")
    return generalInfo

def saveAll(schoolsInfo, pricesInfo, securitiesInfo):
    pass

def execute(abbreviations=None):
    states = []
    if abbreviations == None:
        states = db.getStates()
    else:
        states = [db.getState(abbreviation) for abbreviation in abbreviations]
    schoolsInformations(states)
    # pricesInformations(states)
    # securityInformations(states)
    return True

# execute(['DF'])
# execute(['AC','AL','AM'])
# execute(['SE','SP','TO'])
# execute(['PE','PI','PR'])
execute(['AP','BA','CE'])
# execute(['RR','RS','SC'])
# execute(['MT','PA','PB'])
# execute(['ES','GO','RJ'])
# execute(['RN','RO','MA'])
# execute(['MG','MS'])
