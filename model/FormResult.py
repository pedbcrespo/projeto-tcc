class FormResult:
    def __init__(self, formResult):
        self.title : str = formResult['title']
        self.increase : list = formResult['increase']
        self.decrease : list = formResult['decrease']
        self.answer : int = formResult['answer']
        self.subAttributes : list = formResult['subAttributes']
        self.pontuations : dict = formResult['pontuations']

    def getPontuation(self) -> dict:
        pontuations = self.pontuations
        for key in self.pontuations:
            pontuations[key] = self.pontuations[key][self.answer]
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