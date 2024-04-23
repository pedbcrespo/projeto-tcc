import database as db
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from rpaInternet import RpaInternet
from csvGeneralCity import CsvGeneralCity
import functools as ft
import subprocess
import time


def schoolsInformations(states):        
    infos = []
    rpaSchools = RpaSchools()
    data = None
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS DE ESCOLARIDADE :: {state['abbreviation']} :: {city['name']}")
            points = generalInformation(state, city)['escolaridade']
            data = rpaSchools.execute(state, city)
            if data == None:
                continue
            data.update({'city': city, 'points': points})
            print(f"ESCOLAS {city['name']}:{data['amount']}||{data['rate']}")
            infos.append(data)
    print('FIM DA ITERACAO DOS ESTADOS')
    infos = list(filter(lambda val: val['amount'] != None and val['rate'] != None and val['city'] != None and val['points'] != None, infos))
    try:
        db.saveSchoolsInfo(infos)
        print("DADOS SALVOS COM SUCESSO")
    except Exception as e:
        print("ERRO AO SALVAR", str(e))
    
def pricesInformations(states):
    
    def fixNone(val, infos):
        sameStates = list(filter(lambda x: x['city']['state_id'] == val['city']['state_id'], infos))
        values = list(filter(lambda x: x['price'] != None, sameStates))
        numbers = list(map(lambda x: x['price'], values))
        maxs = list(map(lambda x: x['max_price'], values))
        mins = list(map(lambda x: x['min_price'], values))
        reduce = lambda arr: ft.reduce(lambda a, b: a+b, arr)
        if numbers == []:
            return None
        sum = reduce(numbers)
        sumMax = reduce(maxs)
        sumMin = reduce(mins)
        avg = round(sum/len(numbers), 2)
        sumMax = round(sumMax/len(maxs),2)
        sumMin = round(sumMin/len(mins),2)
        val['price'] = avg
        val['max_price'] = sumMax
        val['min_price'] = sumMin
        return val
        
                
    infos = []
    rpaPrices = RpaPrices()
    for state in states:
        cities = db.getStatesCity(state['abbreviation'])
        for city in cities:
            print(f"COLETANDO DADOS DOS PRECOS :: {state['abbreviation']} :: {city['name']}")
            avgHomePrices, maxPrice, minPrice = rpaPrices.execute(state, city)
            infos.append({'city': city, 'price': avgHomePrices, 'max_price': maxPrice, 'min_price': minPrice})  
    
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
    try:
        db.saveGeneralInfo(city, generalInfo)
        print("DADOS SALVOS COM SUCESSO")
    except:
        print("ERRO AO SALVAR")
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
            # time.sleep(15)
            for i in [0,1]:
                try:
                    avgPrice = rpaInternet.execute(state, city)
                    break
                except:
                    avgPrice = None
                    if i<1:
                        subprocess.Popen(f'start cmd /K type message.txt', shell=True)
                        input('Pressione ENTER para tentar novamente')
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
    pricesInformations(states)
    # schoolsInformations(states)
    # securityInformations(states)
    # internetInformation(states)
    return True



# execute()

# execute(['DF'])
# execute(['RR'])
# execute(['AP'])
# execute(['AC'])
# execute(['RO'])
# execute(['AM'])
# execute(['SE'])
# execute(['ES'])
# execute(['MS'])
# execute(['RJ'])
# execute(['AL'])
# execute(['TO'])
# execute(['MT'])
# execute(['PA'])
# execute(['RN'])
# execute(['CE'])
# execute(['PE'])
# execute(['MA'])
# execute(['PB'])
# execute(['PI'])
# execute(['GO'])
# execute(['SC'])
# execute(['PR'])
# execute(['BA'])
# execute(['RS'])
# execute(['SP'])
# execute(['MG'])


for state in db.getStates():
    for city in db.getStatesCity(state['abbreviation']):
        generalInformation(state, city)