from . import config

orm = config.ormDatabase

class City(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    state_id = config.ormDatabase.Column(config.ormDatabase.Integer, config.ormDatabase.ForeignKey('state.id'))
    def __init__(self, id):
        self.id = id