import functools as ft
from typing import List, Dict
from model.State import State
from model.attributes import Attributes

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
    def __init__(self, ordenationAttributes:Dict[str, int], generalPontuation:Dict[str, Dict], lightPrices: List[float], waterPrices: List[float]):
        self.attributes = {
            Attributes.LIVING_QUALITY: {'pontuation': 1, 'key': 'livingQuality'},
            Attributes.EMPLOYABILITY: {'pontuation': 1, 'key': 'employability'},
            Attributes.LEISURE: {'pontuation': 1, 'key': 'leisure'},
            Attributes.COST: {'pontuation': 1, 'key': 'coust'},
        }

        self.subAttributes = {
            Attributes.HOURS_LIGHT_ESTIMATE: 0,
            Attributes.LT_WATER_CONSUME: 0,
            Attributes.ALIMENTATION: 0,
            Attributes.HYGIENE: 0,
            Attributes.TRANSPORTATION: 0,
            Attributes.HEALTH: 0,
            Attributes.RECREATION: 0
        }

        for key in ordenationAttributes:
            self.attributes[key]['pontuation'] = ordenationAttributes[key]

        for key in generalPontuation:
            avg = generalPontuation[key]['avg']
            print(avg)
            self.subAttributes[key] = avg

        self.pricesLight = lightPrices
        self.pricesWater = waterPrices
        self.limitCoustLiving = None

    def getOrdenationAttributeList(self) -> list:
        return [{"key": self.attributes[attribute]['key'], "value": self.attributes[attribute]['pontuation']} for attribute in self.attributes]

    def getTotal(self, state: State ) -> float:
        currentLightPrice = list(filter(lambda lightPrice: lightPrice['state_id'] == state.id, self.pricesLight))
        currentWaterPrice = list(filter(lambda waterPrice: waterPrice['region_id'] == state.region_id, self.pricesWater))
        
        print('lightPrice', self.pricesLight)
        print('waterPrice', self.pricesWater)

        price = lambda listValue: 0 if len(listValue) == 0 else listValue[0]
        total = price(currentLightPrice) + price(currentWaterPrice)
        for key in self.subAttributes:
            total += self.subAttributes[key]
        return round(total, 2)

    def __str__(self) -> str:
        return f"({self.attributes})"
