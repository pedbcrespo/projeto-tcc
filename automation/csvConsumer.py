import pandas as pd
import database as db

class csvConsumer:
    def __init__(self):
        self.alimentationData = []
        
        
    def get(self, state, type):
        pass
    
    

if __name__ == '__main__':
    dictAlimentation = {
        "Rondônia": 386.79,
        "Acre": 637.28,
        "Amazonas": 557.70,
        "Roraima": 545.88,
        "Pará": 608.43,
        "Amapá": 894.87,
        "Tocantins": 294.00,
        "Maranhão": 498.60,
        "Piauí": 647.17,
        "Ceará": 526.53,
        "Rio Grande do Norte": 820.21,
        "Paraíba": 496.10,
        "Pernambuco": 587.35,
        "Alagoas": 390.71,
        "Sergipe": 794.97,
        "Bahia": 626.61,
        "Minas Gerais": 688.51,
        "Espírito Santo": 465.51,
        "Rio de Janeiro": 596.14,
        "São Paulo": 751.62,
        "Paraná": 641.75,
        "Santa Catarina": 698.67,
        "Rio Grande do Sul": 736.69,
        "Mato Grosso do Sul": 806.48,
        "Mato Grosso": 708.29,
        "Goiás": 652.88,
        "Distrito Federal": 876.27
    }
    
    dictRecreation = {
        "Rondônia": 78.77,
        "Acre": 70.66,
        "Amazonas": 74.59,
        "Roraima": 54.50,
        "Pará": 63.04,
        "Amapá": 83.43,
        "Tocantins": 52.48,
        "Maranhão": 64.16,
        "Piauí": 33.12,
        "Ceará": 54.28,
        "Rio Grande do Norte": 91.19,
        "Paraíba": 75.39,
        "Pernambuco": 72.99,
        "Alagoas": 49.34,
        "Sergipe": 73.72,
        "Bahia": 75.39,
        "Minas Gerais": 95.09,
        "Espírito Santo": 69.96,
        "Rio de Janeiro": 109.07,
        "São Paulo": 122.13,
        "Paraná": 105.92,
        "Santa Catarina": 93.05,
        "Rio Grande do Sul": 112.85,
        "Mato Grosso do Sul": 89.84,
        "Mato Grosso": 82.67,
        "Goiás": 95.56,
        "Distrito Federal": 243.24
    }
    
    dictHealthComsumer = {
        "Rondônia": 169.65,
        "Acre": 153.13,
        "Amazonas": 112.54,
        "Roraima": 108.42,
        "Pará": 149.05,
        "Amapá": 185.96,
        "Tocantins": 134.27,
        "Maranhão": 150.73,
        "Piauí": 170.87,
        "Ceará": 175.37,
        "Rio Grande do Norte": 259.20,
        "Paraíba": 180.42,
        "Pernambuco": 227.17,
        "Alagoas": 186.00,
        "Sergipe": 284.77,
        "Bahia": 252.51,
        "Minas Gerais": 324.49,
        "Espírito Santo": 344.44,
        "Rio de Janeiro": 311.36,
        "São Paulo": 423.96,
        "Paraná": 243.51,
        "Santa Catarina": 295.05,
        "Rio Grande do Sul": 345.63,
        "Mato Grosso do Sul": 293.28,
        "Mato Grosso": 292.38,
        "Goiás": 283.86,
        "Distrito Federal": 650.07
    }
    
    states = db.getStates()
    
    listAlimentation = []
    listRecreation = []
    listHealthConsumer = []
    
    def getDict(id, value):
        return {'state_id':id, 'value':value}
    
    
    for state in states:
        dicState = {'id': state['id'], 'name':state['name']}
        alimentation = dictAlimentation[state['name']]
        recreation = dictRecreation[state['name']]
        healthConsumer = dictHealthComsumer[state['name']]
        
        listAlimentation.append(getDict(state["id"], alimentation))
        listRecreation.append(getDict(state["id"], recreation))
        listHealthConsumer.append(getDict(state["id"], healthConsumer))
    
    # db.saveConsumerData('info_alimentation', listAlimentation)
    db.saveConsumerData('info_recreation', listRecreation)
    db.saveConsumerData('info_health_consumer', listHealthConsumer)
        