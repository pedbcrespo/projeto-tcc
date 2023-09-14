from configuration.dev_configuration import *
import pymysql.cursors
import requests
import os

def getCities(state):
    uf = state['abbreviation']
    response = requests.get(f"{IBGE_BASE_URL}/estados/{uf}/municipios")
    cities = [{'name': city['nome'], 'state_id': state['id']} for city in response.json()]
    return cities

def getDistricts(city):
        districts = []
        response = []
        apiCity = requests.get(f"{DISTRICTS_API_BASE_URL}/{city['name']}")
        if len(apiCity.json()) == 0:
            return []
        response = requests.get(f"{DISTRICTS_API_BASE_URL}/{apiCity.json()[0]['Id']}/bairros")
        districts = [{'name': district['Nome'], 'city_id': city['id']} for district in response.json()]
        return districts

def executa():
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                database=database,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    with connection:
        print('======================================')
        print('DATA BASE CONNECTION:')

        with connection.cursor() as cursor:
            states = []
            cities = []
            districts = []

            sql = 'SELECT * FROM city'
            cursor.execute(sql)
            results = cursor.fetchall()
            cities = [row for row in results]
            count = 0
            sql = "INSERT INTO `district` (`name`, `city_id`) VALUES (%s, %s)"
            for city in cities:
                districts = getDistricts(city)
                count += 1
                values = [(district['name'], district['city_id']) for district in districts]
                cursor.executemany(sql, values)
                os.system('cls')
                print(f"Lendo bairros das cidades: ")
                print(f"{count}/{len(cities)} :: {round((count/len(cities))*100, 2)}%")

        connection.commit()
        
        
