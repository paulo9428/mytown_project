import sys
import os

CURRENT_DIR = os.getcwd()

sys.stdout = sys.stderr
sys.path.insert(0, CURRENT_DIR)

from flaskapp import app as application