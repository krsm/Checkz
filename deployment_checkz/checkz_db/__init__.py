import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from .models import User, SavedPlaces
from .database import db_session, init_db



