import os
import sys

from daily_record import app

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SECRET_KEY = os.getenv('SECRET_KEY', 'secret_string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
UPLOAD_PATH = os.path.join(app.root_path, 'uploads')
