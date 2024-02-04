from database import getStates, getStatesCity, saveEnterprises

import pandas as pd

def readXLSXFile(fileName):
    path = '../csvData/enterprises/' + fileName
    try:
        return pd.read_excel(path, header=None)
    except FileNotFoundError:
        print(f"O arquivo '{path}' não foi encontrado.")
        data = {'0': [],'1': []}
        return pd.DataFrame(data)


def generateDictEnterprises(city, df):
    enterprises = []
    for row in df.itertuples(index=False):
        enterprise = {'city_id': city['id'], 'type_description': row[0]}
        enterprises.append(enterprise)

    amounts = df.iloc[:, 1].tolist()  # Obtém a coluna 1 como uma lista
    for i in range(len(enterprises)):
        enterprises[i]['amount'] = amounts[i]

    print(city['name'], len(enterprises))
    return enterprises


def save():
    states = getStates()
    valuesToSave = []
    for state in states:
        cities = getStatesCity(state['abbreviation'])
        for city in cities:
            fileName = f"{state['abbreviation']}-{city['name']}.xlsx"
            enterprises = []
            df = readXLSXFile(fileName)
            enterprises = generateDictEnterprises(city, df)
            valuesToSave += enterprises

    saveEnterprises(valuesToSave)

if __name__ == '__main__':
    save()