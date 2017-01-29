# -*- coding: utf-8 -*-
import os
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
from flask import Flask
# from .config import configure

# config_name = 'development'
app = Flask('Checkz', static_folder=BASE_DIR + '/static', template_folder=BASE_DIR + '/templates')
# Configurations
app.config.from_pyfile('config.py')

app.config['SECRET_KEY'] = os.urandom(32)

