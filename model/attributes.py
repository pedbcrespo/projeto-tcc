class Attributes:
    HOURS_LIGHT_ESTIMATE = 'hoursLightEstiamte'
    LT_WATER_CONSUME = 'ltWaterConsume'
    ALIMENTATION = 'alimentation'
    HYGIENE = 'hygiene'
    TRANSPORTATION = 'transportation'
    HEALTH = 'health'
    RECREATION = 'recreation'

    LIVING_QUALITY = 'LIVING_QUALITY'
    EMPLOYABILITY = 'EMPLOYABILITY'
    LEISURE = 'LEISURE'
    COST = 'COST'

def getOrdenationAttributeNames():
    return [
        Attributes.LIVING_QUALITY,
        Attributes.EMPLOYABILITY,
        Attributes.LEISURE,
        Attributes.COST 
    ]
    
def getGeneralPontuation():
    return [
        Attributes.HOURS_LIGHT_ESTIMATE,
        Attributes.LT_WATER_CONSUME,
        Attributes.ALIMENTATION,
        Attributes.HYGIENE,
        Attributes.TRANSPORTATION,
        Attributes.HEALTH,
        Attributes.RECREATION
    ]