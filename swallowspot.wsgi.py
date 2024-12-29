import sys

# project directory
project_home = '/var/www/swallowspot.it/SwallowSpot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual enviornement
sys.path.insert(0,"/var/www/swallowspot.it/SwallowSpot/venv/lib/python3.12/site-packages")

# Import your Flask app
from app import app as application