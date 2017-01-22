# instance/config.py
# to be created content
import os

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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # API
    GOOGLE_API = os.environ['GOOGLE_API_KEY']




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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # API
    GOOGLE_API = os.environ['GOOGLE_API_KEY']



# dict with the possible configurations

