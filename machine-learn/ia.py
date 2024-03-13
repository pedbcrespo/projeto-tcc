from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import json

# O quiz vai converter as respostas para valores desses 4 atributos:
#   qualidade de vida
#   empregabilidade
#   lazer
#   custo

examples = []
def readExamples():
    pathJsonFile = './exampleData.json'
    try:
        with open(pathJsonFile, 'r') as arquivo:
            conteudo_json = json.load(arquivo)
        return conteudo_json
    except FileNotFoundError:
        print(f'O arquivo {pathJsonFile} não foi encontrado.')
        return None
    except json.JSONDecodeError:
        print(f'O arquivo {pathJsonFile} não é um arquivo JSON válido.')
        return None

def mostImportantAttribute(df):
    pass