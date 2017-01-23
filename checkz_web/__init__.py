# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from checkz_web.config import configure

config_name = 'development'
app = Flask('Checkz')
app.config.from_object(configure[config_name])

# Flask extensions
db = SQLAlchemy(app)

# def create_app(config_name=None):
#
#     if config_name is None:
#         # TODO CHECKZ_CONFIG to be create as env variable
#         # config_name = os.environ.get('CHECKZ_CONFIG', 'development')

    # config_name = 'development'
    # app = Flask(__name__)
    # app.config.from_object(configure[config_name])

    # #Initialize flask extensions
    # db.init_app(app)

    # return app




