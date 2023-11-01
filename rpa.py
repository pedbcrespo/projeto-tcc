from automation import database
from automation.rpaEscolas import RpaSchools
from automation.rpaPrecos import RpaPrices
from automation.rpaSeguranca import RpaSecurity

states = database.getStates()

for state in states:
    
    cities = database.getStatesCity(state['abbreviation'])
    
    
    

