from configuration.config import ormDatabase

class InfoWaterPriceRegion(ormDatabase.Model):
    region_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('region.id'), primary_key=True)
    price = ormDatabase.Column(ormDatabase.Float)

    def __repr__(self):
        return f"({self.region_id}, {self.price})"

    def json(self):
        return {'region_id': self.region_id, 'price': self.price}