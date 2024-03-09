class attributesPoints:
    def __init__(self):
        self.attributes = {
            'LIVING_QUALITY': 1,
            'EMPLOYABILITY': 1,
            'LEISURE': 1,
            'COUST': 1,
        }

    def add(self, increaseAtt, increaseVal, decreaseAtt, decreaseVal):
        self.attributes[increaseAtt] += increaseAtt if self.attributes[increaseAtt] + increaseVal <= 5 else 5
        self.attributes[decreaseAtt] -= decreaseVal if self.attributes[increaseAtt] - increaseVal >= 1 else 1

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
        'question': "Você tem habito de passear e visitar lugares novos.",
        'attributes': attributes['LEISURE']
    },
    {
        'question': "Vale mais a pena viver proximo aos centros urbanos do que nos subúrbio",
        'attributes': attributes['LIVING_QUALITY']
    },
    {
        'question': "Você procura por novas oportunidades de trabalho.",
        'attributes': attributes['EMPLOYABILITY']
    },
    {
        'question': "Não é tão importante o tamanho do lar, contanto que esteja no seu alcance financeiramente.",
        'attributes': attributes['COUST']
    },
    {
        'question': "Locais movimentados e interessantes são melhores do que o silencio do seu lar.",
        'attributes': attributes['LEISURE']
    },
    {
        'question': "",
        'attributes': attributes['LIVING_QUALITY']
    },
    {
        'question': "Você se considera um profissional de alta qualificação",
        'attributes': attributes['EMPLOYABILITY']
    },
    {
        'question': "Voce prefere grandes centros urbanos á pequenas ou medias cidades",
        'attributes': attributes['COUST']
    },
]