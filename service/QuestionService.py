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
from model.Questions import Question
from model.FormResult import FormResult
from service.InfoService import InfoService
from sqlalchemy import desc, create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft


class QuestionService:

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

    subAttributes = [
        'hoursLightEstiamte',
        'ltWaterConsume',
        'alimentation',
        'hygiene',
        'transportation',
        'health',
        'recreation'
    ]

    def getQuestions(self):
        livingQualityQuestions = [
            self.__generateQuestion__(
                "Você tem habito de gastar mais com produtos que facilitam sua vida.", 
                ['LIVING_QUALITY'], ['COST'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.__generatePontuations__(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você prefere passar mais tempo no conforto de sua casa.",
                ['LIVING_QUALITY'], ['COST'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.__generatePontuations__(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "É melhor pagar mais caro com produtos alimentícios de marcas conhecidas do que as variantes mais baratas.",
                ['LIVING_QUALITY'], ['COST'], ['alimentation'],
                self.__generatePontuations__(['alimentation'])
                ),
            self.__generateQuestion__(
                "É frequente voce se pegar gastando tempo excessivo com cuidados pessoais.",
                ['LIVING_QUALITY'], ['COST'], ['hygiene', 'hoursLightEstiamte', 'ltWaterConsume'],
                self.__generatePontuations__(['hygiene', 'hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você prefere morar mais distante do centro por conta da tranquilidade.",
                ['LIVING_QUALITY'], ['COST'], ['transportation'],
                self.__generatePontuations__(['transportation'])
                ),
            self.__generateQuestion__(
                "É de sua preferencia, ter variedade de clinicas, hospitais e farmacias nas proximidades.",
                ['LIVING_QUALITY'], ['COST'], ['transportation', 'health'],
                self.__generatePontuations__(['transportation', 'health'])
                ),
            self.__generateQuestion__(
                "É interessante para você que haja atividade interessantes para ocupar o tempo o mais proximo o possivel.",
                ['LIVING_QUALITY'], ['COST'], ['recreation'],
                self.__generatePontuations__(['recreation'])
                ),
        ]

        employabilityQuestions = [
            self.__generateQuestion__(
                "Você pode, consegue e prioriza o home office.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.__generatePontuations__(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você gosta de trabalhos com maiores horarios de almoço.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['alimentation'],
                self.__generatePontuations__(['alimentation'])
                ),
            self.__generateQuestion__(
                "É comum, ao voltar do trabalho, você se ve mais sujo que o esperado.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['hygiene'],
                self.__generatePontuations__(['hygiene'])
                ),
            self.__generateQuestion__(
                "Não é incomodo para você que o trabalho seja distante de onde mora.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['transportation'],
                self.__generatePontuations__(['transportation'])
                ),
            self.__generateQuestion__(
                "Você prioriza trabalhos que forneçam melhores planos de saúde.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['health'],
                self.__generatePontuations__(['health'], True)
                ),
            self.__generateQuestion__(
                "É interessante que seu trabalho seja proximo de locais interessantes para se divertir.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['recreation'],
                self.__generatePontuations__(['recreation'])
                ),
        ]

        leisureQuestios = [
            self.__generateQuestion__(
                "Você gosta de objetos de uso domesticos que deixam o ambiente mais moderno.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['hoursLightEstiamte'],
                self.__generatePontuations__(['hoursLightEstiamte'])
                ),
            self.__generateQuestion__(
                "Coisas como piscinas ou banheiras de hidromassagem estão na sua lista de desejos.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['ltWaterConsume'],
                self.__generatePontuations__(['ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você usa muito aplicativos de compras de alimentos, seja de restaurante ou mesmo de compras em supermercados.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['alimentation'],
                self.__generatePontuations__(['alimentation'])
                ),
            self.__generateQuestion__(
                "Cuidar de si, não é apenas uma necessidade, mas algo prazeroso e divertido para você.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['hygiene'],
                self.__generatePontuations__(['hygiene'])
                ),
            self.__generateQuestion__(
                "Você gosta de sair para conhecer lugares novos.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['transportation'],
                self.__generatePontuations__(['transportation'])
                ),
            self.__generateQuestion__(
                "É interessante morar proximo de locais com atividades como yoga, academia, natação ou outras atividades ao ar livre.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['health'],
                self.__generatePontuations__(['health'])
                ),
            self.__generateQuestion__(
                "Você prefere morar proximo de cinemas, restaurantes, parques, entre outros.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['recreation'],
                self.__generatePontuations__(['recreation'])
                ),
        ]

        costQuestions = []


    def __generateQuestion__(self, title, increase, decrease=[], subAttributes=[], pontuations={}):
        return Question(title, increase, decrease, subAttributes, pontuations)

    def __generatePontuations__(self, subAttributes, isReverted=False):
        pontuation = {}
        for att in subAttributes:
            pontuation[att] = self.__calculatePontuation__(att, isReverted)
        return pontuation

    def __calculatePontuation__(self, attribute, isReveted=False):
        valuesAttributes = {
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