# projeto-tcc
# Sistema de Recomendação de Cidades para Habitação: Um estudo de caso do Estado do Rio de Janeiro
## Objetivo:
 Coletar dados da cidade e gerar recomendações de moradia, ou seja, qual seria o bairro mais ideal para o usuario.

## Para executar:
    * Entre no projeto e instale as dependecias listadas no requirements.txt com o comando: 
        pip install -r requirements.txt
    * Certifique-se de que possui o banco de dados MySQL juntamente com o database
    * Para rodar o projeto execute: python main.py

## Fontes das buscas dos dados:
    * Cidades e Estados: https://servicodados.ibge.gov.br/api/docs/localidades#api-Subdistritos-municipiosMunicipioSubdistritosGet
    * Bairros: http://enderecos.metheora.com/Help/Api/GET-api-cidade-id-bairros-q
    * Dados gerais das cidades: https://www.ibge.gov.br/cidades-e-estados.html
    * Dados mais detalhados sobre escolas: http://educacao.dadosabertosbr.org/api
    * Dados sobre quantidade de escolas: https://qedu.org.br/brasil/busca
    * Site de venda de casas e apartamentos: https://www.zapimoveis.com.br/
    * Dados sobre indice de homicidios do ponto de vista internacional: https://homicide.igarape.org.br/?l=es
    * Dados sobre indice de violencia em municipios do ano de 2019: https://infograficos.gazetadopovo.com.br/seguranca-publica/atlas-da-violencia-2019-por-municipios/
    * Dados sobre preços de imoveis: https://www.vivareal.com.br/
    * Dados sobre preços de imoveis: https://www.zapimoveis.com.br/
    * Dados sbore hospitais de todo o país: https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp?search=CABO%20FRIO
    * Dados sobre segurança da sinesp em powerbi: https://app.powerbi.com/view?r=eyJrIjoiYjhhMDMxMTUtYjE3NC00ZjY5LWI5Y2EtZDljNzBlNDg2ZjVkIiwidCI6ImViMDkwNDIwLTQ0NGMtNDNmNy05MWYyLTRiOGRhNmJmZThlMSJ9
    * Tarifas de luz por cidade: https://portalrelatorios.aneel.gov.br/luznatarifa/basestarifas
    * Explicação sobre as tarifas: https://www.webarcondicionado.com.br/tarifa-de-energia-eletrica-kwh-valores-e-ranking-cidades
    * Noticia sobre consumo medio de energia eletrica por individuo: https://jornal.usp.br/noticias/serie-energia-brasil-aparece-entre-os-paises-que-mais-consomem-energia/
    * PDF Com informações sobre consumo de energia eletrica por região: https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-160/topico-168/Fact%20Sheet%20-%20Anu%C3%A1rio%20Estat%C3%ADstico%20de%20Energia%20El%C3%A9trica%202022.pdf
    * Informações sobre o consumo de energia eletrica no Brasil: https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/anuario-estatistico-de-energia-eletrica
    * Informação sobre custo da agua por região: https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/37054-em-2020-para-cada-r-1-00-gerado-pela-economia-foram-consumidos-6-2-litros-de-agua#:~:text=Exclu%C3%ADda%20a%20atividade%20%C3%81gua%20e,%2C09%2Fm%C2%B3%20em%202020.
    * Custo da agua por litro em cada região no Brasil: https://fusatiambiental.com.br/o-custo-da-agua-no-brasil/
    * Noticia sobre consumo de agua por regiao: https://exame.com/brasil/onde-mais-se-consome-agua-no-brasil/
    * Consumo medio de agua por pessoa no Brasil: https://site.sabesp.com.br/site/interna/Default.aspx?secaoId=140#:~:text=De%20acordo%20com%20a%20Organiza%C3%A7%C3%A3o,mais%20de%20200%20litros%2Fdia.
    * Consumo medio de agua em litros por dia por pessoa em cada estado do Brasil: https://datasan-ibre.fgv.br/comparativo/estados
    * Noticia sobre preço medio da internet no Brasil: https://gizmodo.uol.com.br/preco-medio-banda-larga-brasil-por-mbps/
    * Noticia sobre banda media de internet por região no Brasil: https://www.telesintese.com.br/pesquisa-de-campo-levanta-precos-do-acesso-a-internet-brasileira/
    * Tabelas de IPCA de algumas regioes do pais: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html?=&t=resultados
    * site de comparação de planos de internet por cidade: https://melhorplano.net/internet-banda-larga
    * tabela sobre consumo de alimentação e outros pontos: https://cidades.ibge.gov.br/brasil/pesquisa/46/84498
    * site que calcula media geral do custo de vido no Brasil: https://www.expatistan.com/pt/custo-de-vida/pais/brasil
    * informações sobre empresas no país, com especificação por cidade: https://www.econodata.com.br/empresas/todo-brasil
    * projeção grafica de empresas no país: https://public.tableau.com/app/profile/mapadeempresas/viz/MapadeEmpresasnoBrasil_15877433181480/VisoGeral