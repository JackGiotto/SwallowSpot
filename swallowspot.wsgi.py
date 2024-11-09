import sys
import os

# project directory
project_home = '/var/www/SwallowSpot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual enviornement
sys.path.insert(0,"/var/www/SwallowSpot/venv/lib/python3.11/site-packages")

# Import your Flask app
from app import app as application