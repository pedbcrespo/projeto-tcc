import functools as ft
ANSWER_ALTERNATIVES = 5

class AttributesPoints:
    def __init__(self):
        self.attributes = {
            'LIVING_QUALITY': 1,
            'EMPLOYABILITY': 1,
            'LEISURE': 1,
            'COST': 1,
        }

        self.attributesEquilavence = {
            'LIVING_QUALITY': 'livingQuality',
            'EMPLOYABILITY': 'employability',
            'LEISURE': 'leisure',
            'COST': 'coust',
        }

        self.subAttributes = [
            'hoursLightEstiamte',
            'ltWaterConsume',
            'alimentation',
            'hygiene',
            'transportation',
            'health',
            'recreation'
        ]

        self.pricesLight = []
        self.pricesWater = []
        self.limitCoustLiving = None
        
    def add(self, increase, decrease, val):
        for key in increase:
            self.attributes[key] += (val - increase.index(key))
        for key in decrease:
            decreasePoints = decrease.index(key)
            self.attributes[key] -= decreasePoints
            if self.attributes[key] < 1:
                self.attributes[key] = 1

    def getList(self):
        return [{"key": key, "value": self.attributes[key]} for key in self.attributes]

    def getTotal(self):
        pricesLight = list(map(lambda priceLight: priceLight['price'], self.pricesLight))
        pricesWater = list(map(lambda priceWater: priceWater['price'], self.pricesWater))
        avgPriceLight = ft.reduce(lambda a,b : a+b, pricesLight)/len(self.pricesLight)
        avgPriceWater = ft.reduce(lambda a,b : a+b, pricesWater)/len(self.pricesWater)
        return avgPriceLight + avgPriceWater + self.limitCoustLiving

    def __costCalculation__(self, costPoints):
        pass

    def __str__(self):
        return f"({self.attributes})"
def generateQuestion(title, increase, decrease=[], subAttributes=[]):
    return  {
        'title': title,
        'increase': increase,
        'decrease': decrease,
        'subAttributes': subAttributes
    }

questions = [
    generateQuestion("É de sua preferencia viver mais proximo do centro.", 
                     ['LIVING_QUALITY', 'LEISURE'], ['COST'], 
                     ['transportation', 'health', 'recreation', 'alimentation']),
    generateQuestion("Ter onde trabalhar é mais importante que sair com os amigos ou familia", 
                     ['EMPLOYABILITY', 'COST'], ['LEISURE', 'LIVING_QUALITY'],
                    ),
    generateQuestion("Você tem habito de passear e visitar lugares novos.", 
                     ['LEISURE'], ['COST'],
                     ['transportation', 'recreation']),
    generateQuestion("Você não se importa com o quão espaçoso é o seu lar.", 
                     ['COST'],
                     ),
    generateQuestion("Você prefere morar proximo de locais mais movimentados e interessantes de se visitar.", 
                     ['LEISURE'], ['LIVING_QUALITY', 'COST', 'EMPLOYABILITY'],
                     ['recreation', 'transportation', 'alimentation']),
    generateQuestion("Você frequentemente gasta com produtos e serviços que tornam sua vida mais facil ou pratica.",
                     ['LIVING_QUALITY'], ['COST'],
                     ['health', 'hoursLightEstiamte', 'ltWaterConsume']),
    generateQuestion("Estar proximo de possiveis oportunidades de emprego é uma de suas prioridades.",
                     ['EMPLOYABILITY'], ['LEISURE'],
                     ['transportation']),
    generateQuestion("Voce prefere pequenas ou medias cidades ao invés de grandes metrópoles.", 
                     ['COST'], ['LIVING_QUALITY'],
                     ['hoursLightEstiamte','ltWaterConsume','alimentation','hygiene','transportation','health','recreation']),
    generateQuestion("Você frequentemente sai para ir em eventos de sua cidade.", 
                     ['LEISURE', 'LIVING_QUALITY'], ['COST', 'EMPLOYABILITY'],
                     ['recreation', 'transportation', 'alimentation']),
    generateQuestion("Prefere uma vida equilibrada, valoriza a qualidade de vida.", 
                     ['LIVING_QUALITY', 'LEISURE'], ['COST'],
                     ['alimentation', 'hygiene', 'health', 'recreation']),
    generateQuestion("Frequentemente tem o habito de procurar por vagas de trabalho nas proximidades de onde mora.", 
                     ['EMPLOYABILITY'], ['LEISURE'],
                     ['transportation']),
    generateQuestion("Você não se incomoda com a localidade no qual vive contanto que sobre mais dinheiro no final do mês para gastar com o que quer.", 
                     ['COST', 'LEISURE'], ['LIVING_QUALITY'],
                     ['transportation', 'recreation', 'health']),
    generateQuestion("Nas suas compras, você compra os preza a qualidade, mesmo que isso signifique pagar mais por eles.", 
                     ['LIVING_QUALITY', 'LEISURE'],['COST']
                     ['alimentation', 'hygiene', 'health']),
    generateQuestion("Você ou outras pessoas da sua casa fazem tratamentos médicos que demandam compra de muita medicação.", 
                     ['LIVING_QUALITY'],[],
                     ['health']),
    generateQuestion("No seu horário em casa, você utiliza muitos eletrodomésticos ou aparelhos que possuem alto potencial de consumo de energia elétrica.", 
                     ['LIVING_QUALITY'],[],
                     ['hoursLightEstiamte']),
    generateQuestion("Você costuma lavar roupas, louça ou áreas específicas da casa com muita frequência.", 
                     ['COST'],[],
                     ['ltWaterConsume']),
    generateQuestion("Durante o dia, sua casa costuma ter pouca gente ou ninguém.", 
                     ['LIVING_QUALITY'],[],
                     ['hoursLightEstiamte']),
    generateQuestion("Normalmente você leva muito tempo para tomar banho.", 
                     ['COST'],[],
                     ['hoursLightEstiamte']),
]