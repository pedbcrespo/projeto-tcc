from model.InfoLightConsume import InfoLightConsume
from model.InfoWaterConsumer import InfoWaterConsumer
from model.InfoCoustLiving import InfoCoustLiving
from model.Questions import Question
from model.attributes import Attributes
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from configuration.config import conn


class QuestionService:
    def getQuestions(self):
        livingQualityQuestions = [
            self.__generateQuestion__(
                "Você tem habito de gastar mais com produtos que facilitam sua vida.", 
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME])
                ),
            self.__generateQuestion__(
                "Você prefere passar mais tempo no conforto de sua casa.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME])
                ),
            self.__generateQuestion__(
                "É melhor pagar mais caro com produtos alimentícios de marcas conhecidas do que as variantes mais baratas.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.ALIMENTATION],
                self.generatePontuations([Attributes.ALIMENTATION])
                ),
            self.__generateQuestion__(
                "É frequente voce se pegar gastando tempo excessivo com cuidados pessoais.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.HYGIENE, Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.HYGIENE, Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME])
                ),
            self.__generateQuestion__(
                "Você prefere morar mais distante do centro por conta da tranquilidade.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.TRANSPORTATION],
                self.generatePontuations([Attributes.TRANSPORTATION])
                ),
            self.__generateQuestion__(
                "É de sua preferencia, ter variedade de clinicas, hospitais e farmacias nas proximidades.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.TRANSPORTATION, Attributes.HEALTH],
                self.generatePontuations([Attributes.TRANSPORTATION, Attributes.HEALTH])
                ),
            self.__generateQuestion__(
                "É interessante para você que haja atividade interessantes para ocupar o tempo o mais proximo o possivel.",
                [Attributes.LIVING_QUALITY], [Attributes.COST], [Attributes.RECREATION],
                self.generatePontuations([Attributes.RECREATION])
                ),
        ]

        employabilityQuestions = [
            self.__generateQuestion__(
                "Você pode, consegue e prioriza o home office.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME])
                ),
            self.__generateQuestion__(
                "Você gosta de trabalhos com maiores horarios de almoço.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.ALIMENTATION],
                self.generatePontuations([Attributes.ALIMENTATION])
                ),
            self.__generateQuestion__(
                "É comum, ao voltar do trabalho, você se ve mais sujo que o esperado.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.HYGIENE],
                self.generatePontuations([Attributes.HYGIENE])
                ),
            self.__generateQuestion__(
                "Não é incomodo para você que o trabalho seja distante de onde mora.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.TRANSPORTATION],
                self.generatePontuations([Attributes.TRANSPORTATION])
                ),
            self.__generateQuestion__(
                "Você prioriza trabalhos que forneçam melhores planos de saúde.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.HEALTH],
                self.generatePontuations([Attributes.HEALTH], True)
                ),
            self.__generateQuestion__(
                "É interessante que seu trabalho seja proximo de locais interessantes para se divertir.", 
                [Attributes.EMPLOYABILITY], [Attributes.LEISURE], [Attributes.RECREATION],
                self.generatePontuations([Attributes.RECREATION])
                ),
        ]

        leisureQuestios = [
            self.__generateQuestion__(
                "Você gosta de objetos de uso domesticos que deixam o ambiente mais moderno.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.HOURS_LIGHT_ESTIMATE],
                self.generatePontuations([Attributes.HOURS_LIGHT_ESTIMATE])
                ),
            self.__generateQuestion__(
                "Coisas como piscinas ou banheiras de hidromassagem estão na sua lista de desejos.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.LT_WATER_CONSUME])
                ),
            self.__generateQuestion__(
                "Você usa muito aplicativos de compras de alimentos, seja de restaurante ou mesmo de compras em supermercados.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.ALIMENTATION],
                self.generatePontuations([Attributes.ALIMENTATION])
                ),
            self.__generateQuestion__(
                "Cuidar de si, não é apenas uma necessidade, mas algo prazeroso e divertido para você.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.HYGIENE],
                self.generatePontuations([Attributes.HYGIENE])
                ),
            self.__generateQuestion__(
                "Você gosta de sair para conhecer lugares novos.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.TRANSPORTATION],
                self.generatePontuations([Attributes.TRANSPORTATION])
                ),
            self.__generateQuestion__(
                "É interessante morar proximo de locais com atividades como yoga, academia, natação ou outras atividades ao ar livre.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.HEALTH],
                self.generatePontuations([Attributes.HEALTH])
                ),
            self.__generateQuestion__(
                "Você prefere morar proximo de cinemas, restaurantes, parques, entre outros.", 
                [Attributes.LEISURE], [Attributes.EMPLOYABILITY], [Attributes.RECREATION],
                self.generatePontuations([Attributes.RECREATION])
                ),
        ]

        costQuestions = [
            self.__generateQuestion__(
                "Você se considera uma pessoa regrada quanto ao consumo de água e luz.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME],
                self.generatePontuations([Attributes.HOURS_LIGHT_ESTIMATE, Attributes.LT_WATER_CONSUME], True)
                ),
            self.__generateQuestion__(
                "Para você, é melhor um almoço barato do que chique.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.ALIMENTATION],
                self.generatePontuations([Attributes.ALIMENTATION], True)
                ),
            self.__generateQuestion__(
                "Higiene pessoal é uma necessidade e apenas isso.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.HYGIENE],
                self.generatePontuations([Attributes.HYGIENE], True)
                ),
            self.__generateQuestion__(
                "Você, sempre que possivel, prefere meios alternativos para se locomover.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.TRANSPORTATION],
                self.generatePontuations([Attributes.TRANSPORTATION], True)
                ),
            self.__generateQuestion__(
                "A saúde depente unica e exclusivamente da forma que você vive.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.HEALTH],
                self.generatePontuations([Attributes.HEALTH], True)
                ),
            self.__generateQuestion__(
                "Você concorda com a frase de uma música do Charlie Brown Jr: ``Muita gente se diverte com o que tem``.", 
                [Attributes.COST], [Attributes.LIVING_QUALITY], [Attributes.RECREATION],
                self.generatePontuations([Attributes.RECREATION], True)
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
            Attributes.HOURS_LIGHT_ESTIMATE: self.__getMaxAndMinLightConsume__(InfoLightConsume.amount),
            Attributes.LT_WATER_CONSUME: self.__getMaxAndMinWaterConsume__(InfoWaterConsumer.amount),
            Attributes.ALIMENTATION: self.__getMaxAndMinCostLiving__(Attributes.ALIMENTATION),
            Attributes.HYGIENE: self.__getMaxAndMinCostLiving__(Attributes.HYGIENE),
            Attributes.TRANSPORTATION: self.__getMaxAndMinCostLiving__(Attributes.TRANSPORTATION),
            Attributes.HEALTH: self.__getMaxAndMinCostLiving__(Attributes.HEALTH),
            Attributes.RECREATION: self.__getMaxAndMinCostLiving__(Attributes.RECREATION)
        }

        maxAndMin = valuesAttributes[attribute]
        avg = round((maxAndMin['max'] + maxAndMin['min']) / 2, 2)
        avgMax = round((maxAndMin['max'] + avg) / 2, 2)
        avgMin = round((avg + maxAndMin['min']) / 2, 2)

        pontuation = [maxAndMin['min'], avgMin, avg, avgMax, maxAndMin['max']]
        return pontuation if not isReveted else pontuation.reverse()


    def __getMaxAndMinCostLiving__(self, columnName):
        attribute = {
            Attributes.ALIMENTATION: InfoCoustLiving.alimentation,
            Attributes.TRANSPORTATION: InfoCoustLiving.transport,
            Attributes.HEALTH: InfoCoustLiving.health,
            Attributes.HYGIENE: InfoCoustLiving.hygiene,
            Attributes.RECREATION: InfoCoustLiving.recreation,
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