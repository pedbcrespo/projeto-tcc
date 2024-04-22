from typing import Dict

class FormResult:
    def __init__(self, formResult):
        print("FORM RESULT", formResult['pontuations'])
        self.title : str = formResult['title']
        self.increase : list = formResult['increase']
        self.decrease : list = formResult['decrease']
        self.answer : int = formResult['answer']
        self.subAttributes : list = formResult['subAttributes']
        self.pontuations : Dict[str, list] = formResult['pontuations']
    
    def getPontuation(self, key: str) -> int:
        print('GET PONTUATION', key)
        print(self.pontuations[key])
        pos : int = self.answer - 1
        print("POS", pos)
        pontuation : int = self.pontuations[key][pos]
        return pontuation
    
    def json(self) -> dict:
        return {
            "title": self.title,
            "increase": self.increase,
            "decrease": self.decrease,
            "pontuations": self.getPontuations(),
        }
    def __str__(self) -> str:
        return f"({self.title}, {self.increase}, {self.decrease}, {self.answer}, {self.pontuations})"