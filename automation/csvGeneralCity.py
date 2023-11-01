import pandas as pd
import database as db

class CsvGeneralCity:
    def readingStateCsv(self, uf):
        fileName = f"csvData/{uf}-todos-municipios.csv"
        dataframe = pd.read_csv(fileName, skiprows=[0], encoding='utf-8')
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
        dataframe = dataframe.drop(columns=['unnamed', 'prefeito', 'nome_nascente'])
        numericColumns = [
            'area_territorial(km²)',
            'populacao_residente',
            'densidade_demografica',
            'escolaridade',
            'idh',
            'receitas_realizadas',
            'despesas_empenhadas',
            'pib_per_capta'
        ]
        for column in numericColumns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')
            media = dataframe[column].mean()
            dataframe[column].fillna(media, inplace=True)
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
        columns = [column for column in dataframe.columns]
        rowDf = dataframe[dataframe['codigo'] == f"{ibgeCityId}"]
        return self.dataframeJson(rowDf, columns)
    
    

state = db.getState('RJ')
cities = db.getStatesCity(state['abbreviation'])

csvReader = CsvGeneralCity()
print(csvReader.getDataOfCity(state['abbreviation'], cities[0]['ibge_id']))
