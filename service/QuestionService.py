from model.InfoLightConsume import InfoLightConsume
from model.InfoWaterConsumer import InfoWaterConsumer
from model.InfoCoustLiving import InfoCoustLiving
from model.Questions import Question
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn


class QuestionService:
    def getQuestions(self):
        livingQualityQuestions = [
            self.__generateQuestion__(
                "Você tem habito de gastar mais com produtos que facilitam sua vida.", 
                ['LIVING_QUALITY'], ['COST'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.generatePontuations(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você prefere passar mais tempo no conforto de sua casa.",
                ['LIVING_QUALITY'], ['COST'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.generatePontuations(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "É melhor pagar mais caro com produtos alimentícios de marcas conhecidas do que as variantes mais baratas.",
                ['LIVING_QUALITY'], ['COST'], ['alimentation'],
                self.generatePontuations(['alimentation'])
                ),
            self.__generateQuestion__(
                "É frequente voce se pegar gastando tempo excessivo com cuidados pessoais.",
                ['LIVING_QUALITY'], ['COST'], ['hygiene', 'hoursLightEstiamte', 'ltWaterConsume'],
                self.generatePontuations(['hygiene', 'hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você prefere morar mais distante do centro por conta da tranquilidade.",
                ['LIVING_QUALITY'], ['COST'], ['transportation'],
                self.generatePontuations(['transportation'])
                ),
            self.__generateQuestion__(
                "É de sua preferencia, ter variedade de clinicas, hospitais e farmacias nas proximidades.",
                ['LIVING_QUALITY'], ['COST'], ['transportation', 'health'],
                self.generatePontuations(['transportation', 'health'])
                ),
            self.__generateQuestion__(
                "É interessante para você que haja atividade interessantes para ocupar o tempo o mais proximo o possivel.",
                ['LIVING_QUALITY'], ['COST'], ['recreation'],
                self.generatePontuations(['recreation'])
                ),
        ]

        employabilityQuestions = [
            self.__generateQuestion__(
                "Você pode, consegue e prioriza o home office.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.generatePontuations(['hoursLightEstiamte', 'ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você gosta de trabalhos com maiores horarios de almoço.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['alimentation'],
                self.generatePontuations(['alimentation'])
                ),
            self.__generateQuestion__(
                "É comum, ao voltar do trabalho, você se ve mais sujo que o esperado.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['hygiene'],
                self.generatePontuations(['hygiene'])
                ),
            self.__generateQuestion__(
                "Não é incomodo para você que o trabalho seja distante de onde mora.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['transportation'],
                self.generatePontuations(['transportation'])
                ),
            self.__generateQuestion__(
                "Você prioriza trabalhos que forneçam melhores planos de saúde.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['health'],
                self.generatePontuations(['health'], True)
                ),
            self.__generateQuestion__(
                "É interessante que seu trabalho seja proximo de locais interessantes para se divertir.", 
                ['EMPLOYABILITY'], ['LEISURE'], ['recreation'],
                self.generatePontuations(['recreation'])
                ),
        ]

        leisureQuestios = [
            self.__generateQuestion__(
                "Você gosta de objetos de uso domesticos que deixam o ambiente mais moderno.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['hoursLightEstiamte'],
                self.generatePontuations(['hoursLightEstiamte'])
                ),
            self.__generateQuestion__(
                "Coisas como piscinas ou banheiras de hidromassagem estão na sua lista de desejos.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['ltWaterConsume'],
                self.generatePontuations(['ltWaterConsume'])
                ),
            self.__generateQuestion__(
                "Você usa muito aplicativos de compras de alimentos, seja de restaurante ou mesmo de compras em supermercados.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['alimentation'],
                self.generatePontuations(['alimentation'])
                ),
            self.__generateQuestion__(
                "Cuidar de si, não é apenas uma necessidade, mas algo prazeroso e divertido para você.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['hygiene'],
                self.generatePontuations(['hygiene'])
                ),
            self.__generateQuestion__(
                "Você gosta de sair para conhecer lugares novos.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['transportation'],
                self.generatePontuations(['transportation'])
                ),
            self.__generateQuestion__(
                "É interessante morar proximo de locais com atividades como yoga, academia, natação ou outras atividades ao ar livre.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['health'],
                self.generatePontuations(['health'])
                ),
            self.__generateQuestion__(
                "Você prefere morar proximo de cinemas, restaurantes, parques, entre outros.", 
                ['LEISURE'], ['EMPLOYABILITY'], ['recreation'],
                self.generatePontuations(['recreation'])
                ),
        ]

        costQuestions = [
            self.__generateQuestion__(
                "Você se considera uma pessoa regrada quanto ao consumo de água e luz.", 
                ['COST'], ['LIVING_QUALITY'], ['hoursLightEstiamte', 'ltWaterConsume'],
                self.generatePontuations(['hoursLightEstiamte', 'ltWaterConsume'], True)
                ),
            self.__generateQuestion__(
                "Para você, é melhor um almoço barato do que chique.", 
                ['COST'], ['LIVING_QUALITY'], ['alimentation'],
                self.generatePontuations(['alimentation'], True)
                ),
            self.__generateQuestion__(
                "Higiene pessoal é uma necessidade e apenas isso.", 
                ['COST'], ['LIVING_QUALITY'], ['hygiene'],
                self.generatePontuations(['hygiene'], True)
                ),
            self.__generateQuestion__(
                "Você, sempre que possivel, prefere meios alternativos para se locomover.", 
                ['COST'], ['LIVING_QUALITY'], ['transportation'],
                self.generatePontuations(['transportation'], True)
                ),
            self.__generateQuestion__(
                "A saúde depente unica e exclusivamente da forma que você vive.", 
                ['COST'], ['LIVING_QUALITY'], ['health'],
                self.generatePontuations(['health'], True)
                ),
            self.__generateQuestion__(
                "Você concorda com a frase de uma música do Charlie Brown Jr: ``Muita gente se diverte com o que tem``.", 
                ['COST'], ['LIVING_QUALITY'], ['recreation'],
                self.generatePontuations(['recreation'], True)
                ),
        ]

        questions = livingQualityQuestions + employabilityQuestions + leisureQuestios + costQuestions
        return [question.json() for question in questions]

    def __generateQuestion__(self, title, increase, decrease=[], subAttributes=[], pontuations={}):
        return Question(title, increase, decrease, subAttributes, pontuations)

    def generatePontuations(self, subAttributes, isReverted=False):
        pontuation = {}
        for att in subAttributes:
            pontuation[att] = self.__calculatePontuation__(att, isReverted)
        return pontuation

    def __calculatePontuation__(self, attribute, isReveted=False):
        valuesAttributes = {
            'hoursLightEstiamte': self.__getMaxAndMinLightConsume__(InfoLightConsume.amount),
            'ltWaterConsume': self.__getMaxAndMinWaterConsume__(InfoWaterConsumer.amount),
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
            'transportation': InfoCoustLiving.transport,
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
        return {'max': float(result[0]), 'min': float(result[1])}

    def __getMaxAndMinLightConsume__(self, attribute):
        with self.__createSession__() as session:
            query = session.query(
                func.max(func.round(attribute / 12, 2)).label('max'),
                func.min(func.round(attribute / 12, 2)).label('min')
            )
            result = query.one()
            return {'max': float(result.max), 'min': float(result.min)}
    
    def __getMaxAndMinWaterConsume__(self, attribute):
        with self.__createSession__() as session:
            query = session.query(
                func.max(func.round(attribute, 2)).label('max'),
                func.min(func.round(attribute, 2)).label('min')
            )
            result = query.one()
            return {'max': float(result.max), 'min': float(result.min)}


    def __createSession__(self):
        engine = create_engine(conn)
        Session = sessionmaker(bind=engine)
        return Session()