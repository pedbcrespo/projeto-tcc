import pymysql.cursors
import re
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

def executeWrite(query):
    connection = getConnection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
        try:
            connection.commit()
            return True
        except:
            print(f"ERRO AO EXECUTAR {query}")
            return False

def getAllCities():
    return execute('SELECT * FROM city ORDER BY name')

def getStates():
    return execute('SELECT * FROM state ORDER BY name')

def getStateById(stateId):
    return execute(f"SELECT * FROM state WHERE id = {stateId}")

def getState(abbreviation):
    state = execute(f'SELECT * FROM state WHERE abbreviation = "{abbreviation}"')
    return state[0] if state != None else None

def getStatesCity(abbreviation):
    state = getState(abbreviation)
    if not state:
        return []
    return execute(f"SELECT * FROM city WHERE state_id = {state['id']} ORDER BY name")

def saveSchoolsInfo(infos):
    infoQuery = list(map(lambda x: f"({x['city']['id']}, {x['amount']}, {x['rate']}, {x['points']})", infos))
    query = f'INSERT IGNORE INTO info_schools (city_id, amount_schools, scholarity_rate, points) VALUES {",".join(infoQuery)}'
    executeWrite(query)
    return True

def saveSecurityInfo(infos):
    infoQuery = list(map(lambda x: f"({x['city']['id']}, {x['rate']})", infos))
    print('========================= QUERY =========================')
    print(",".join(infoQuery))
    print('=========================================================')
    query = f'INSERT IGNORE INTO info_security (city_id, rate) VALUES {",".join(infoQuery)}'
    executeWrite(query)
    return True
    
def savePricesInfo(infos):
    infoQuery = list(map(lambda x: f"({x['city']['id']}, {x['price']})", infos))
    query = f'INSERT INTO info_prices (city_id, avg_price) VALUES {",".join(infoQuery)}'
    executeWrite(query)
    return True

def saveInternetInfo(infos):
    infoQuery = list(map(lambda x: f"({x['city']['id']}, {x['avgPrice']})", infos))
    query = f'INSERT INTO info_internet (city_id, avg_price) VALUES {",".join(infoQuery)}'
    executeWrite(query)
    return True

def saveGeneralInfo(city, generalInfo):
    def convertType(value, typedef, function=None):
        if value == None or value == '-':
            return None
        res = typedef(re.sub(r'[().]', '', f"{value}"))
        return res if function == None else function(res)
    
    pibPerCapta = round(generalInfo['pib_per_capta'], 2)
    population = convertType(generalInfo['populacao_residente'], int)
    idh = round(float(generalInfo['idh']), 2)
    demographicDensity = round(float(generalInfo['densidade_demografica']), 2)
    print(f'({city["id"]}, {pibPerCapta}, {population}, {idh}, {demographicDensity})', type(idh))
    query = f'INSERT INTO info_general (city_id, idhm, population, idh, demographic_density) VALUES ({city["id"]}, {pibPerCapta}, {population}, {idh}, {demographicDensity})'
    executeWrite(query)
    return generalInfo


def saveConsumerData(tableName, values):
    querySql = ','.join(list(map(lambda x: f"{x['state_id'], x['value']}", values)))
    print(querySql)
    sql = f"INSERT INTO {tableName} (state_id, avg_price) VALUES {querySql}"
    return executeWrite(sql)
    
def saveEnterprises(values):
    query = ','.join(list(map(lambda x: f"{x['city_id']}, '{x['type_description']}', {x['amount']}", values)))
    print(query)
    sql = f"INSERT INTO info_enterprises (city_id, type_description, amount) VALUES {query}"
    return executeWrite(sql)