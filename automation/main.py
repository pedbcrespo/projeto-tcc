import database as db
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from rpaInternet import RpaInternet
from csvGeneralCity import CsvGeneralCity
import functools as ft
import time


def schoolsInformations(states):
    infos = []
    rpaSchools = RpaSchools()
    data = None
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
        print(infos)
        print(data)
    
def pricesInformations(states):
    
    def fixNone(val, infos):
        sameStates = list(filter(lambda x: x['city']['state_id'] == val['city']['state_id'], infos))
        values = list(filter(lambda x: x['price'] != None, sameStates))
        numbers = list(map(lambda x: x['price'], values))
        if numbers == []:
            return None
        sum = ft.reduce(lambda a, b: a+b, numbers)
        avg = round(sum/len(numbers), 2)
        val['price'] = avg
        return val
        
                
    infos = []
    rpaPrices = RpaPrices()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS DOS PRECOS :: {state['abbreviation']} :: {city['name']}")
            avgHomePrices = rpaPrices.execute(state, city)
            infos.append({'city': city, 'price': avgHomePrices})  
    
    infos = list(map(lambda val: fixNone(val, infos), infos))
    try:
        db.savePricesInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except Exception as e:
        print("ERRO AO SALVAR", str(e))
        print(infos)

def securityInformations(states):
    infos = []
    rpaSecurity = RpaSecurity()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS SEGURANCA :: {state['abbreviation']} :: {city['name']}")
            securityRate = rpaSecurity.execute(state, city)
            infos.append({'city':city, 'rate': securityRate['rate']})
    try:
        db.saveSecurityInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except Exception as e:
        print("ERRO AO SALVAR", str(e))
        # print(infos)

def generalInformation(state, city):
    generalCsv = CsvGeneralCity()
    generalInfo = generalCsv.execute(state, city)
    # try:
    #     db.saveGeneralInfo(city, generalInfo)
    #     print("DADOS SALVOS COM SUCESSO")
    # except:
    #     print("ERRO AO SALVAR")
    return generalInfo

def internetInformation(states):
    def fixNoneCases(data, infos):
        if data['avgPrice'] != None:
            return data
        avgPricesCity = list(map(lambda x: x['avgPrice'], infos))
        avgWithoutNones = list(filter(lambda x: x != None, avgPricesCity))
        sum = ft.reduce(lambda a, b: a+b, avgWithoutNones)
        avg = round(sum/len(avgWithoutNones), 2)
        data['avgPrice'] = avg
        return data
    infos = []
    rpaInternet = RpaInternet()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            for i in [0,1]:
                try:
                    avgPrice = rpaInternet.execute(state, city)
                    break
                except:
                    if i<1:
                        input('Observe o SITE, depois pressione ENTER para tentar novamente')
            info = {'city': city, 'avgPrice': avgPrice}
            infos.append(info)
            print(city['name'], avgPrice, f"{cities.index(city)+1}/{len(cities)}")
        infos = list(map(lambda info: fixNoneCases(info, infos), infos))
        db.saveInternetInfo(infos)
    return True

def execute(abbreviations=None):
    states = []
    if abbreviations == None:
        states = db.getStates()
    else:
        states = [db.getState(abbreviation) for abbreviation in abbreviations]
    # schoolsInformations(states)
    # pricesInformations(states)
    # securityInformations(states)
    internetInformation(states)
    return True



# execute()

# execute(['DF'])
# execute(['AC'])
# execute(['AL'])
# execute(['AP'])
# execute(['AM'])
# execute(['SE'])
# execute(['ES'])
# execute(['RJ'])
# execute(['TO'])
# execute(['RN'])
# execute(['CE'])
# execute(['PE'])
execute(['MA'])
# execute(['SP'])
# execute(['PI'])
# execute(['PR'])
# execute(['BA'])
# execute(['RR'])
# execute(['RS'])
# execute(['SC'])
# execute(['MT'])
# execute(['PA'])
# execute(['PB'])
# execute(['GO'])
# execute(['RO'])
# execute(['MS'])
# execute(['MG'])
