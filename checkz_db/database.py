import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# DB_NAME = 'checkz.db'
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR)


PATH_DB = 'sqlite:///' + BASE_DIR + '/checkz.db'

engine = create_engine(PATH_DB, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from checkz_db import models
    Base.metadata.create_all(bind=engine)
#
if __name__ == "__main__":

    init_db()