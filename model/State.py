from configuration import config

orm = config.ormDatabase

class State(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(100))
    abbreviation = orm.Column(orm.String(2))
    state_id = orm.Column(orm.Integer, orm.ForeignKey('state.id'))