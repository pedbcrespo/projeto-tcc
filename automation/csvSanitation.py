from database import getAllCities, saveSanitation
import pandas as pd
import os

def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def percent(val, total):
   if val % 5 == 0:
    clear()
    print(round((val/total)*100, 2), '%')

def readFile(filePath):
    try:
        csvData = pd.read_csv(filePath, delimiter=';')
        return csvData
    except FileNotFoundError:
        print(f"O arquivo '{filePath}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV '{filePath}': {e}")

def floatConvert(val):
  if val == 'Atendimento Pleno':
    return 0
  try:
    return float(val.replace(',', '.').replace('%', ''))
  except:
    return -1 


def save():
    df = readFile('../csvData/sanitation/municipiose_saneamento_export.csv')
    chosenColumns = ['Cidade', 'Possui Plano Municipal', 'População sem Água', 'População sem Esgoto', 'População sem coleta de lixo']
    dictFunctions = {
        'População sem Água': lambda val: floatConvert(val),
        'População sem Esgoto': lambda val: floatConvert(val),
        'População sem coleta de lixo': lambda val: floatConvert(val)
    }

    equivalentColumn = {
        'Possui Plano Municipal': 'has_municipal_plan',
        'População sem Água': 'population_no_water',
        'População sem Esgoto': 'population_no_sewage',
        'População sem coleta de lixo': 'population_no_garbage_collection'
    }

    listRows = []
    cities = getAllCities()
    total = len(df)
    count = 0
    for row in df[chosenColumns].iterrows():
        percent(count, total)
        currentRow = row[1]
        try:
          city = list(filter(lambda x: x['name'] == currentRow['Cidade'], cities))[0]
        except:
           continue
        dictRow = {'city_id': city['id']}
        for col in chosenColumns:
          if col in equivalentColumn:
            dictRow[equivalentColumn[col]] = dictFunctions[col](currentRow[col]) if col in dictFunctions else currentRow[col]
        listRows.append(dictRow)
        count += 1
    percent(count, total)
    print('SALVANDO...')
    saveSanitation(listRows)
    print('PROCESSO FINALIZADO')




if __name__ == '__main__':
    save()