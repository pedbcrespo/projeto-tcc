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

    def __costCalculation__(self, costPoints):
        pass

    def __str__(self):
        return f"({self.attributes})"
def generateQuestion(title, increase, decrease=[]):
    return  {
        'title': title,
        'increase': increase,
        'decrease': decrease,
    }

questions = [
    generateQuestion("É de sua preferencia viver mais proximo do centro.", ['LIVING_QUALITY', 'LEISURE'], ['COST']),
    generateQuestion("Ter onde trabalhar é mais importante que sair com os amigos ou familia", ['EMPLOYABILITY', 'COST'], ['LEISURE', 'LIVING_QUALITY']),
    generateQuestion("Você tem habito de passear e visitar lugares novos.", ['LEISURE'], ['COST']),
    generateQuestion("Você não se importa com o quão espaçoso é o seu lar.", ['COST']),
    generateQuestion("Você prefere morar proximo de locais mais movimentados e interessantes de se visitar.", ['LEISURE'], ['LIVING_QUALITY', 'COST', 'EMPLOYABILITY']),
    generateQuestion("Você frequentemente gasta com produtos e serviços que tornam sua vida mais facil ou pratica.", ['LIVING_QUALITY'], ['COST']),
    generateQuestion("Estar proximo de possiveis oportunidades de emprego é uma de suas prioridades.", ['EMPLOYABILITY'], ['LEISURE']),
    generateQuestion("Voce prefere pequenas ou medias cidades ao invés de grandes metrópoles.", ['COST'], ['LIVING_QUALITY']),
    generateQuestion("Você frequentemente sai para ir em eventos de sua cidade.", ['LEISURE', 'LIVING_QUALITY'], ['COST', 'EMPLOYABILITY']),
    generateQuestion("Prefere uma vida equilibrada, valoriza a qualidade de vida.", ['LIVING_QUALITY', 'LEISURE'], ['COST']),
    generateQuestion("Frequentemente tem o habito de procurar por vagas de trabalho nas proximidades de onde mora.", ['EMPLOYABILITY'], ['LEISURE']),
    generateQuestion("Você não se incomoda com a localidade no qual vive contanto que sobre mais dinheiro no final do mês para gastar com o que quer.", ['COST', 'LEISURE'], ['LIVING_QUALITY']),
]