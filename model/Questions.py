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
        'title': "A qualidade de vida é mais importante do que a distancia ate o centro urbano.",
        'attribute': 'LIVING_QUALITY'
    },
    {
        'title': "Ter onde trabalhar é mais importante que sair com os amigos e familia",
        'attribute': 'EMPLOYABILITY'
    },
    {
        'title': "O tamanho do lar não é tão relevante quanto a praticidade do local aonde mora.",
        'attribute': 'COUST'
    },
    {
        'title': "Locais movimentados e interessantes do que a variedade de vagas de trabalho na cidade.",
        'attribute': 'LEISURE'
    },
    {
        'title': "Você tem como prioridade gastar mais por mais praticidade e conforto.",
        'attribute': 'LIVING_QUALITY'
    },
    {
        'title': "Você se considera um profissional de alta qualificação",
        'attribute': 'EMPLOYABILITY'
    },
    {
        'title': "Voce prefere grandes centros urbanos á pequenas ou medias cidades",
        'attribute': 'COUST'
    },
]