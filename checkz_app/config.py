# instance/config.py
# to be created content
import os

# related to geo functions
RADIUS_CIRCLE = 3  # distance used to be same place in meters
RADIUS_SAVED_PLACES = 241402  # 15 miles  = 24.1402 considering closed places in radius

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEV_DB_NAME = "dev_checkz.db"

PROD_DB_NAME = "checkz.db"

class BaseConfig(object):
    # Statement for enabling the development environment
    DEBUG = False
    # # Secret key for signing cookies
    SECRET_KEY = os.urandom(32)
    # # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # # Use a secure, unique and absolutely secret key for
    # # signing the data.
    CSRF_SESSION_KEY = os.urandom(32)
    # # Application threads. A common general assumption is
    # # using 2 per available processor cores - to handle
    # # incoming requests using one and performing background
    # # operations using the other.
    THREADS_PER_PAGE = 2
    # # Define the database - we are working with
    # # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, PROD_DB_NAME)
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # API
    # GOOGLE_API = os.environ['GOOGLE_API_KEY']

    GOOGLE_API_KEY = "AIzaSyCy1rfaC4-cM1rSTNgd-XXXOV15qt9vUb0;"

class DevelopmentConfig(BaseConfig):

    # Statement for enabling the development environment
    DEBUG = True
    # # Secret key for signing cookies
    SECRET_KEY = os.urandom(32)
    # # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # # Use a secure, unique and absolutely secret key for
    # # signing the data.
    CSRF_SESSION_KEY = os.urandom(32)
    # # Application threads. A common general assumption is
    # # using 2 per available processor cores - to handle
    # # incoming requests using one and performing background
    # # operations using the other.
    THREADS_PER_PAGE = 2
    # # Define the database - we are working with
    # # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DEV_DB_NAME)
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # API
    # GOOGLE_API = os.environ['GOOGLE_API_KEY']

    GOOGLE_API_KEY = "AIzaSyCy1rfaC4-cM1rSTNgd-XXXOV15qt9vUb0;"



# dict with the possible configurations

configure = {

    'development': "checkz_app.config.DevelopmentConfig",
    'default': 'checkz_app.config.DevelopmentConfig',
    'deployment': 'checkz_app.config.BaseConfig'

}


# def configure_app(app):
#
#     config_name = "development"
#     app.config.from_object(config[config_name])
#