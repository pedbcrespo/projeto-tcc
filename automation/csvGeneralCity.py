import pandas as pd
import database as db

class CsvGeneralCity:
    def __init__(self):
        self.selectedColumns = []
        
    def readingStateCsv(self, uf):
        fileName = f"csvData/{uf}-todos-municipios.csv"
        dataframe = pd.read_csv(fileName, skiprows=[0,-1], encoding='utf-8')
        dataframe = dataframe.rename(columns={
            'Munic&iacute;pio [-]': 'municipio',
            'C&oacute;digo [-]': 'codigo',
            'Gent&iacute;lico [-]': 'nome_nascente',
            'Prefeito [2021]': 'prefeito',
            '&Aacute;rea Territorial - km&sup2; [2022]': 'area_territorial(km²)',
            'Popula&ccedil;&atilde;o residente - pessoas [2022]': 'populacao_residente',
            'Densidade demogr&aacute;fica - hab/km&sup2; [2022]': 'densidade_demografica',
            'Escolariza&ccedil;&atilde;o &lt;span&gt;6 a 14 anos&lt;/span&gt; - % [2010]': 'escolaridade',
            'IDHM &lt;span&gt;&Iacute;ndice de desenvolvimento humano municipal&lt;/span&gt; [2010]': 'idh',
            'Mortalidade infantil - &oacute;bitos por mil nascidos vivos [2020]': 'mortalidade_infantil',
            'Receitas realizadas - R$ (&times;1000) [2017]': 'receitas_realizadas',
            'Despesas empenhadas - R$ (&times;1000) [2017]': 'despesas_empenhadas',
            'PIB per capita - R$ [2020]':'pib_per_capta',
            'Unnamed: 13': 'unnamed'
        })
        dataframe = dataframe.drop(columns=['municipio', 'unnamed', 'prefeito', 'nome_nascente', 'despesas_empenhadas'], errors='ignore')
        numericColumns = [
            'area_territorial(km²)',
            'populacao_residente',
            'densidade_demografica',
            'escolaridade',
            'idh',
            'receitas_realizadas',
            'pib_per_capta'
        ]
        for column in numericColumns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')
            media = dataframe[column].mean()
            dataframe[column].fillna(media, inplace=True)
            
        self.selectedColumns = ['codigo', 'area_territorial(km²)', 'populacao_residente', 'densidade_demografica', 'escolaridade', 'idh', 'receitas_realizadas', 'pib_per_capta']
        return dataframe
        
    def dataframeJson(self, row, columns):
        dictRow = {}
        values = row.values[0]
        index = 0
        for column in columns:
            if column == 'codigo':
                continue
            dictRow[column] = values[index]
            index += 1
        return dictRow
    
    def getDataOfCity(self, uf, ibgeCityId):
        dataframe = self.readingStateCsv(uf)
        row = dataframe[dataframe['codigo'] == f"{ibgeCityId}"]
        columns = row[self.selectedColumns]
        return self.dataframeJson(row, columns)
    
    def execute(self, state, city):
        uf = state['abbreviation']
        ibgeCityId = city['ibge_id']
        try: 
            return self.getDataOfCity(uf, ibgeCityId)
        except:
            print(f'ERRO AO BUSCAR DADOS DO {state["abbreviation"]} - {city["name"]}')
            return None
        
states = db.getStates()
csvReader = CsvGeneralCity()
for state in states:
    cities = db.getStatesCity(state['abbreviation'])
    for city in cities:
        print(csvReader.execute(state, city))
