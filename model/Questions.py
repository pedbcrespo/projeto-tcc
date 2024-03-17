class AttributesPoints:
    def __init__(self):
        self.attributes = {
            'LIVING_QUALITY': 1,
            'EMPLOYABILITY': 1,
            'LEISURE': 1,
            'COUST': 1,
        }

    def __relationIncreaseDecrease__(self, attribute, val):
        relation = {
            'LIVING_QUALITY': {'decrease': 'COUST', 'percent': 0.5},
            'EMPLOYABILITY': {'decrease': 'LEISURE', 'percent': 0.5},
            'LEISURE': {'decrease': 'EMPLOYABILITY', 'percent': 0.5},
            'COUST': {'decrease': 'LIVING_QUALITY', 'percent': 0.5},
        }
        decrease = relation[attribute]['decrease']
        valueToSub = round(val * relation[attribute]['percent'])
        return decrease, valueToSub
    
    def add(self, increaseAtt, val):
        decreaseAtt, valToSub = self.__relationIncreaseDecrease__(increaseAtt, val)
        self.attributes[increaseAtt] += val 
        self.attributes[decreaseAtt] = self.attributes[decreaseAtt] - valToSub if self.attributes[decreaseAtt] - valToSub >= 1 else 1

    def getList(self):
        return [{"key": key, "value": self.attributes[key]} for key in self.attributes]
    
attributes = {
    'LIVING_QUALITY': 'livingQuality',
    'EMPLOYABILITY': 'employability',
    'LEISURE': 'leisure',
    'COUST': 'coust',
}

questions = [
    {
        'title': "Você tem habito de passear e visitar lugares novos.",
        'attribute': 'LEISURE'
    },
    {
        'title': "É de sua preferencia viver mais proximo do centro.",
        'attribute': 'LIVING_QUALITY'
    },
    {
        'title': "Ter onde trabalhar é mais importante que sair com os amigos e familia",
        'attribute': 'EMPLOYABILITY'
    },
    {
        'title': "Você não se importa com o quão espaçoso é o seu lar.",
        'attribute': 'COUST'
    },
    {
        'title': "Você prefere morar proximo de locais mais movimentados e interessantes de se visitar.",
        'attribute': 'LEISURE'
    },
    {
        'title': "Você frequentemente gasta com produtos e serviços que tornam sua vida mais facil ou pratica.",
        'attribute': 'LIVING_QUALITY'
    },
    {
        'title': "Estar proximo de possiveis oportunidades de emprego é uma de suas prioridades.",
        'attribute': 'EMPLOYABILITY'
    },
    {
        'title': "Voce prefere grandes centros urbanos á pequenas ou medias cidades",
        'attribute': 'COUST'
    },
    {
        'title': "Você frequentemente sai para ir em eventos de sua cidade.",
        'attribute': 'LEISURE'
    },
    {
        'title': "Prefere uma vida equilibrada, valoriza a qualidade de vida.",
        'attribute': 'LIVING_QUALITY'
    },
    {
        'title': "Frequentemente tem o habito de procurar por vagas de trabalho nas proximidades de onde mora.",
        'attribute': 'EMPLOYABILITY'
    },
    {
        'title': "Você não se incomoda com a localidade no qual vive contanto que sobre mais dinheiro no final do mês para gastar com o que quer.",
        'attribute': 'COUST'
    },
]