# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from checkz_app.config import configure

# Flask extensions
db = SQLAlchemy()

from checkz_app.models import User, SavedPlaces


def create_app(config_name=None):

    if config_name is None:
        # TODO CHECKZ_CONFIG to be create as env variable
        # config_name = os.environ.get('CHECKZ_CONFIG', 'development')
        config_name = 'development'

    app = Flask(__name__)
    app.config.from_object(configure[config_name])

    #Initialize flask extensions
    db.init_app(app)

    return app




