
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_NAME = 'checkz.db'
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQL_ALCHEMY_URI = 'sqlite:///' + os.path.join(BASE_DIR, DB_NAME)

engine = create_engine(SQL_ALCHEMY_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import checkz_data.models
    Base.metadata.create_all(bind=engine)