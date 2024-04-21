import functools as ft
from State import State
ANSWER_ALTERNATIVES = 5

class Question:
    def __init__(self, title, increase, decrease=[], subAttributes=[], pontuations={}):
        self.title = title
        self.increase = increase
        self.decrease = decrease
        self.subAttributes = subAttributes
        self.pontuations = pontuations

    def json(self):
        return {
            'title': self.title,
            'increase': self.increase,
            'decrease': self.decrease,
            'subAttributes': self.subAttributes,
            'pontuations': self.pontuations
        }


class AttributesPoints:
    def __init__(self, ordenationAttributes:dict, generalPontuation:dict):
        self.attributes = {
            'LIVING_QUALITY': {'pontuation': 1, 'key': 'livingQuality'},
            'EMPLOYABILITY': {'pontuation': 1, 'key': 'employability'},
            'LEISURE': {'pontuation': 1, 'key': 'leisure'},
            'COST': {'pontuation': 1, 'key': 'coust'},
        }

        self.subAttributes = [
            {'hoursLightEstiamte': 0},
            {'ltwaterConsume': 0},
            {'alimentation': 0},
            {'hygiene': 0},
            {'transportation': 0},
            {'health': 0},
            {'recreation': 0}
        ]

        for key in ordenationAttributes:
            self.attributes[key]['pontuation'] = ordenationAttributes[key]

        for key in generalPontuation:
            self.subAttributes[key] = generalPontuation[key]['avg']

        self.pricesLight = []
        self.pricesWater = []
        self.limitCoustLiving = None

    def getOrdenationAttributeList(self) -> list:
        return [{"key": attribute['key'], "value": self.attributes[attribute]['pontuation']} for attribute in self.attributes]

    def getTotal(self, state: State ) -> float:
        currentLightPrice = list(filter(lambda lightPrice: lightPrice['state_id'] == state.id))
        currentWaterPrice = list(filter(lambda waterPrice: waterPrice['region_id'] == state.region_id))
        total = currentLightPrice + currentWaterPrice
        for key in self.subAttributes:
            total += self.subAttributes[key]
        return round(total, 2)

    def __str__(self) -> str:
        return f"({self.attributes})"
