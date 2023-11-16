
class FormAttributes:
    def __init__(self, priceRate, coustLivingPriceRate, typeCitySize):
        self.priceRate = priceRate
        self.coustLivingPriceRate = coustLivingPriceRate
        self.typeCitySize = typeCitySize
        
    def __str__(self):
        return f"({self.priceRate}, {self.coustLivingPriceRate}, {self.typeCitySize})"