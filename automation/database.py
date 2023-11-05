import pymysql.cursors
from config import *

def getConnection():
    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                database=database,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

def execute(query):
    result = None
    connection = getConnection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            result = [row for row in results]
    return result

def getStates():
    return execute('SELECT * FROM state')

def getState(abbreviation):
    state = execute(f'SELECT * FROM state WHERE abbreviation = "{abbreviation}"')
    return state[0] if state != None else None

def getStatesCity(abbreviation):
    state = getState(abbreviation)
    if not state:
        return []
    return execute(f"SELECT * FROM city WHERE state_id = {state['id']}")

def saveSchoolsInfo(city, amountSchools, scholarityRate):
    query = f'INSERT INTO info_schools (city_id, amount_schools, scholarity_rate) VALUES ({city["id"]}, {amountSchools}, {scholarityRate})'
    return execute(query)

def saveSecurityInfo(city, securityRate):
    query = f'INSERT INTO info_security (city_id, secutiry_rate) VALUES ({city["id"]},{securityRate})'
    return execute(query)
    
def savePricesInfo(city, avgHomePrices):
    query = f'INSERT INTO info_prices (city_id, avg_homes_price) VALUES ({city["id"]},{avgHomePrices})'
    return execute(query)
    
def saveGeneralInfo(city, generalInfo):
    query = f'INSERT INTO info_general (city_id, pib_per_capta, population, idh, demographic_density)'
    return execute(query)