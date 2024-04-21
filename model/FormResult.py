class FormResult:
    def __init__(self, formResult):
        self.title : str = formResult['title']
        self.increase : list = formResult['increase']
        self.decrease : list = formResult['decrease']
        self.answer : int = formResult['answer']
        self.subAttributes : list = formResult['subAttributes']
        self.pontuations : dict = formResult['pontuations']
    def getPontuation(self) -> dict:
        pontuations = {}
        for key in self.pontuations:
            pos = self.answer - 1
            pontuations.update({key: self.pontuations[key][pos]})
        return pontuations
    
    def json(self) -> dict:
        return {
            "title": self.title,
            "increase": self.increase,
            "decrease": self.decrease,
            "pontuations": self.getPontuation(),
        }
    def __str__(self) -> str:
        return f"({self.title}, {self.increase}, {self.decrease}, {self.answer}, {self.getPontuation()})"