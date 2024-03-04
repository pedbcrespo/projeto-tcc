from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db
from flask_cors import CORS

statisticsFunction = db.CITY_EDUCATION_STATISTIC_BASE_URL

conn = "mysql+pymysql://{}:{}@{}/{}".format(db.user, db.password, db.host, db.database)

app = Flask('__name__')
CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = conn

ormDatabase = SQLAlchemy(app)
api = Api(app)