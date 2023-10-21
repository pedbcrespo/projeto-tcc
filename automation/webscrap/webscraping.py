import requests
from bs4 import BeautifulSoup

url = 'https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.find('div', class_='_container_16i18_1')
    if target_div:
        print(target_div)
    else:
        print("Div não encontrada.")
else:
    print("Falha ao acessar a página. Código de status:", response.status_code)
