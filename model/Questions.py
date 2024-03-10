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
        valueToSub = val * relation[attribute]['percent']
        return decrease, valueToSub
    
    def add(self, increaseAtt, val):
        decreaseAtt, valToSub = self.__relationIncreaseDecrease__(increaseAtt, val)
        self.attributes[increaseAtt] += val if self.attributes[increaseAtt] + val <= 5 else 5
        self.attributes[decreaseAtt] -= valToSub if self.attributes[decreaseAtt] - valToSub >= 1 else 1

    def get(self):
        return self.livingQuality, self.employability, self.leisure, self.coust

textQuestions = [
    "Voce tem habito de passear e visitar lugares novos.",
    "Voce valoriza morar mais proximo do centro da cidade.",
    "Voce procura por novas oportunidades de trabalho.",
    "O conforto do lar é mais importante que opções de serviços da cidade.",
    "Voce costuma sair muito e ficar ate altas horas da noite fora de casa."
]

attributes = {
    'LIVING_QUALITY': 'livingQuality',
    'EMPLOYABILITY': 'employability',
    'LEISURE': 'leisure',
    'COUST': 'coust',
}

questions = [
    {
        'title': "Você tem habito de passear e visitar lugares novos.",
        'attribute': attributes['LEISURE']
    },
    {
        'title': "A qualidade de vida é mais importante do que a distancia ate o centro urbano.",
        'attribute': attributes['LIVING_QUALITY']
    },
    {
        'title': "Ter onde trabalhar é mais importante que sair com os amigos e familia",
        'attribute': attributes['EMPLOYABILITY']
    },
    {
        'title': "O tamanho do lar não é tão relevante quanto a praticidade do local aonde mora.",
        'attribute': attributes['COUST']
    },
    {
        'title': "Locais movimentados e interessantes do que a variedade de vagas de trabalho na cidade.",
        'attribute': attributes['LEISURE']
    },
    {
        'title': "Você tem como prioridade gastar mais por mais praticidade e conforto.",
        'attribute': attributes['LIVING_QUALITY']
    },
    {
        'title': "Você se considera um profissional de alta qualificação",
        'attribute': attributes['EMPLOYABILITY']
    },
    {
        'title': "Voce prefere grandes centros urbanos á pequenas ou medias cidades",
        'attribute': attributes['COUST']
    },
]