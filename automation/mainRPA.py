import database
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from csvGeneralCity import CsvGeneralCity

states = database.getStates()
generalCsv = CsvGeneralCity()
rpaPrices = RpaPrices()
rpaSchools = RpaSchools()
rpaSecurity = RpaSecurity()

dataList = []

for state in states:    
    data = {}
    cities = database.getStatesCity(state['abbreviation'])
    for city in cities:
        print(state['abbreviation'], city['name'])
        data['other_general'] = generalCsv.getDataOfCity(state['abbreviation'], city['ibge_id'])
        data['security_rate'] = rpaSecurity.executa(state, city)
        data['amount_schools'] = rpaSchools.executa(state, city['name'])
        data['avarage_prices'] = rpaPrices.executa(state, city)
        dataList.append(data)
print(dataList)

