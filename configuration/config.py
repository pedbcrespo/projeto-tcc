from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db

statisticsFunction = db.CITY_EDUCATION_STATISTIC_BASE_URL

conn = "mysql+pymysql://{}:{}@{}/{}".format(db.user, db.password, db.host, db.database)

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['CORS_HEADERS'] = 'Content-Type'

ormDatabase = SQLAlchemy(app)
api = Api(app)
CORS(app)