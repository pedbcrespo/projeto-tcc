import database as db
import requests

class ApiEmpresas:
    def __init__(self):
        self.cnpjList = []
        self.url = 'https://portaldatransparencia.gov.br/pessoa-juridica/busca/resultado'

    def __getHeader__(self):
        return {
            'content-type': 'application/json',
        }

    def execute(self):
        # page = 1
        params = {'tamanhoPagina': 1000}
        headers = self.__getHeader__()
        for page in range(1, 3):
            params['pagina'] = page
            res = requests.get(self.url, params=params, headers=headers)
            print(res.headers)
            print(res.status_code)


if __name__ == '__main__':
    api = ApiEmpresas()
    api.execute()