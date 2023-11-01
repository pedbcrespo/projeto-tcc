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


    