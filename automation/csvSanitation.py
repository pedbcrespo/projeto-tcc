from database import getStates, getStatesCity, saveEnterprises
import pandas as pd

def readFile(filePath):
    try:
        csvData = pd.read_csv(filePath, delimiter=';')
        return csvData
    except FileNotFoundError:
        print(f"O arquivo '{filePath}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV '{filePath}': {e}")

def save(csvData):
    pass