import pandas as pd
import database as db

class csvAlimentacao:
    def __init__(self):
        self.alimentationData = []
        
        
    def readCsv(self):
        fileName = 'csvData\alimentation\dados-consumo-ibge.csv'
        dataframe = pd.read_csv(fileName, encoding='utf-8')