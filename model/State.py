from configuration.config import ormDatabase

class State(ormDatabase.Model):
    id = ormDatabase.Column(ormDatabase.Integer, primary_key=True)
    name = ormDatabase.Column(ormDatabase.String(100))
    abbreviation = ormDatabase.Column(ormDatabase.String(2))

    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.abbreviation})"

    def json(self):
        return {'id': self.id, 'name': self.name, 'abbreviation': self.abbreviation}