user='projetotcc'
password='tcc#2023'
host='localhost'
database='tcc_project'

IBGE_BASE_URL = 'https://servicodados.ibge.gov.br/api/v1/localidades'
DISTRICTS_API_BASE_URL = 'http://enderecos.metheora.com/api/cidade/'
BASE_URL = '/info-api'

def CITY_EDUCATION_STATISTIC_BASE_URL(abbreviation, ibgeId):
    return f"http://educacao.dadosabertosbr.org/api/estatisticas?tipoLocal=EST&nomeLocal={abbreviation}&codMunicipio={ibgeId}&indice=0"