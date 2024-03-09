from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd

# O quiz vai converter as respostas para valores desses 4 atributos:
#   qualidade de vida
#   empregabilidade
#   lazer
#   custo

def generateUserAnswersType(livingQuality, employability, leisure, coust, mostImportantAttribute):
    return {
       'livingQuality': livingQuality,
       'employability': employability,
       'leisure': leisure,
       'coust': coust,
       'mostImportantAttribute': mostImportantAttribute
    }

examples = [
    generateUserAnswersType(5,1,1,1, 'livingQuality'),
    generateUserAnswersType(1,5,1,1, 'employability'), 
    generateUserAnswersType(1,1,5,1, 'leisure'), 
    generateUserAnswersType(1,1,1,5, 'coust'),
    generateUserAnswersType(4,2,4,3, 'livingQuality'),
    generateUserAnswersType(2,4,3,4, 'employability'),
    generateUserAnswersType(2,1,4,4, 'leisure'),
    generateUserAnswersType(3,1,3,4, 'coust'),
    generateUserAnswersType(5,1,5,4, 'livingQuality'),
    generateUserAnswersType(3,5,5,4, 'employability'),
    generateUserAnswersType(3,1,5,3, 'leisure'),
    generateUserAnswersType(2,4,1,5, 'coust') 
]

def mostImportantAttribute(df):
    pass