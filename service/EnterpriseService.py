from model.InfoEnterprise import InfoEnterprise
from model.InfoSchools import InfoSchools

class EnterpriseService:
    def getTypeDescriptions(self, cityId):
        typeDescriptions = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).all()
        return [info.type_description for info in typeDescriptions]

    def getAvgProfissionalQualification(self, cityId):
        enterprisesInfo = InfoEnterprise.query.filter(InfoEnterprise.city_id == cityId).all()
        jsonEnterprisesInfo = [info.json() for info in enterprisesInfo]