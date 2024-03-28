class FormResult:
    def __init__(self, formResult):
        self.title = formResult['title']
        self.increase = formResult['increase']
        self.decrease = formResult['decrease']
        self.answer = formResult['answer']
        self.hoursLightEstiamte = formResult['hoursLightEstiamte']
        self.ltWaterConsume = formResult['ltWaterConsume']
        self.alimentation = formResult['alimentation']
        self.hygiene = formResult['hygiene']
        self.transportation = formResult['transportation']
        self.health = formResult['health']
        self.recreation = formResult['recreation']

    def costLivingAttJson(self):
        return {
            'hoursLightEstiamte': self.hoursLightEstiamte,
            'ltWaterConsume': self.ltWaterConsume,
            'alimentation': self.alimentation,
            'hygiene': self.hygiene,
            'transportation': self.transportation,
            'health': self.health,
            'recreation': self.recreation
        }
    
    def __str__(self):
        return f"({self.title}, {self.increase}, {self.decrease}, {self.answer}, {self.hoursLightEstiamte}, {self.ltWaterConsume}, {self.alimentation}, {self.hygiene}, {self.health}, {self.transportation})"