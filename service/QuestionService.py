from model.City import City
from model.State import State
from model.InfoSecurity import InfoSecurity
from model.InfoSchools import InfoSchools
from model.InfoGeneral import InfoGeneral
from model.InfoPrices import InfoPrices
from model.InfoLightConsume import InfoLightConsume
from model.InfoLightPrice import InfoLightPrice
from model.InfoWaterConsumer import InfoWaterConsumer
from model.InfoWaterPriceRegion import InfoWaterPriceRegion
from model.InfoInternet import InfoInternet
from model.InfoCoustLiving import InfoCoustLiving
from model.InfoSanitation import InfoSanitation
from model.InfoEnterprise import InfoEnterprise
from model.Questions import AttributesPoints
from model.FormResult import FormResult
from service.InfoService import InfoService
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft


class QuestionService:
    subAttributes = [
        'hoursLightEstiamte',
        'ltWaterConsume',
        'alimentation',
        'hygiene',
        'transportation',
        'health',
        'recreation'
    ]

    categoryQuestions = [
        'LIVING_QUALITY',
        'EMPLOYABILITY',
        'LEISURE',
        'COST',
    ]

    attributesEquilavence = {
        'LIVING_QUALITY': 'livingQuality',
        'EMPLOYABILITY': 'employability',
        'LEISURE': 'leisure',
        'COST': 'coust',
    }

    def getQuestions(self):
        livingQualityQuestions = [
            self.__generateQuestion__()
        ]

        employabilityQuestions = []

        leiisureQuestios = []

        costQuestions = []


    def __generateQuestion__(self, title, increase, decrease=[], subAttributes=[], pontuations={}):
        return {
            "title": title,
            "increase": increase,
            "decrease": decrease,
            "subAttributes": subAttributes,
            "pontuations": pontuations
        }

    def __calculatePontuation__(self, attribute, isReveted=False):
        valuesAttributes ={
            'hoursLightEstiamte': self.__getMaxAndMin__(InfoLightConsume.amount),
            'ltWaterConsume': self.__getMaxAndMin__(InfoWaterConsumer.amount),
            'alimentation': self.__getMaxAndMinCostLiving__('alimentation'),
            'hygiene': self.__getMaxAndMinCostLiving__('hygiene'),
            'transportation': self.__getMaxAndMinCostLiving__('transportation'),
            'health': self.__getMaxAndMinCostLiving__('health'),
            'recreation': self.__getMaxAndMinCostLiving__('recreation')
        }

        maxAndMin = valuesAttributes[attribute]
        avg = round((maxAndMin['max'] + maxAndMin['min']) / 2, 2)
        avgMax = round((maxAndMin['max'] + avg) / 2, 2)
        avgMin = round((avg + maxAndMin['min']) / 2, 2)

        pontuation = [maxAndMin['min'], avgMin, avg, avgMax, maxAndMin['max']]
        return pontuation if not isReveted else pontuation.reverse()


    def __getMaxAndMinCostLiving__(self, columnName):
        attribute = {
            'alimentation': InfoCoustLiving.alimentation,
            'transport': InfoCoustLiving.transport,
            'health': InfoCoustLiving.health,
            'hygiene': InfoCoustLiving.hygiene,
            'recreation': InfoCoustLiving.recreation,
        }

        with self.__createSession__() as session:
            query = session.query(
            func.max(attribute[columnName]).label('max'),
            func.min(attribute[columnName]).label('min')
        )   
        result = query.one()
        return {'max': result[0], 'min': result[1]}

    def __getMaxAndMin__(self, attribute):
        with self.__createSession__() as session:
            query = session.query(
                func.max(func.round(attribute / 12, 2)).label('max'),
                func.min(func.round(attribute / 12, 2)).label('min')
            )
            result = query.one()
            return {'max': result.max, 'min': result.min}


    def __createSession__(self):
        engine = create_engine(conn)
        Session = sessionmaker(bind=engine)
        return Session()