
import sys
import os.path

from .database import *
from .models import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print(sys.path)