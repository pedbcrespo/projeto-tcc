import database as db
from rpaEscolas import RpaSchools
from rpaPrecos import RpaPrices
from rpaSeguranca import RpaSecurity
from csvGeneralCity import CsvGeneralCity

states = db.getStates()
generalCsv = CsvGeneralCity()
rpaPrices = RpaPrices()
rpaSchools = RpaSchools()
rpaSecurity = RpaSecurity()

dataList = []

def schoolsInformations(state, city, general_info):
    scholarityRate = general_info['escolaridade']
    amountSchools = rpaSchools.executa(state, city)
    db.saveSchoolsInfo(city, amountSchools, scholarityRate)
    
    
def pricesInformation(state, city, general_info):
    avgHomePrices = rpaPrices.executa(state, city)
    db.savePricesInfo(city, avgHomePrices)

def securityInformation(state, city):
    securityRate = rpaSecurity.executa(state, city)
    db.saveSecurityInfo(city, securityRate)

def generalInformation(state, city):
    generalInfo = generalCsv.execute(state, city)
    db.saveGeneralInfo(city, generalInfo)
    return generalInfo

for state in states:    
    cities = db.getStatesCity(state['abbreviation'])
    for city in cities:
        print(state['abbreviation'], city['name'])
        general_info = generalInformation(state, city)
        securityInformation(state, city)
        schoolsInformations(state, city, general_info)
        pricesInformation(state, city, general_info)
        


