from configuration import config

orm = config.ormDatabase

class City(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))