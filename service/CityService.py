from model.City import City
from model.State import State
from model.District import District
from configuration.config import ormDatabase
from typing import List
import pandas as pd

class CityService:
    def getAllCities(self):
        cities = City.query.all()
        cities = [self.setDistricts(city) for city in cities]
        return [city for city in cities]
    
    def getCities(self, uf):
        state = State.query.filter(State.abbreviation == uf).first()
        dataframe = self.readingStateCsv(state.abbreviation.lower())
        cities = City.query.filter(City.state_id == state.id).all()
        cities = [self.setDetailsInfo(city, state, dataframe) for city in cities]
        return [city for city in cities] 
    
    def saveCities(self, cities:List[City]):
        ormDatabase.session.add_all(cities)
        ormDatabase.session.commit()
        return [city.json() for city in cities] 
    
    def setDetailsInfo(self, city:City, state:State, dataframe):
        columns = [column for column in dataframe.columns]
        rowDf = dataframe[dataframe['codigo'] == f"{city.ibge_id}"]
        districts = District.query.filter(District.city_id == city.id).all()
        city.districts = districts
        self.dataframeJson(rowDf, columns)
        city.info = self.dataframeJson(rowDf, columns)
        return city.json()       
        
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
        dataframe = dataframe.drop(columns=['unnamed', 'municipio', 'prefeito', 'nome_nascente', 'mortalidade_infantil'])       
        return dataframe
    
    
    def dataframeJson(self, row, columns):
        dictRow = {}
        values = row.values[0]
        index = 0
        for column in columns:
            if column == 'codigo':
                continue
            dictRow[column] = self.handleContent(values[index], column)
            index += 1
        return dictRow
            
    def handleContent(self, content, column) :
        if content in ['-']:
            return None
        operationsDict = {
            'populacao_residente': lambda ct: ct.replace('.',''),
        }
        if column in operationsDict.keys():
            content = operationsDict[column](content)           
        return round(float(content), 2) if '.' in content else int(content)