import os
from os import getenv

from openwebpos.utils import gen_urlsafe_token

SECRET_KEY = gen_urlsafe_token(16)
DEBUG = getenv('DEBUG', False)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# database
DIALECT = getenv('DB_DIALECT', 'sqlite')
DRIVER = None
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
HOST = getenv('DB_HOST')
PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')

if DIALECT == 'sqlite':
    db_uri = 'sqlite:///' + os.path.join(os.getcwd(), 'openwebpos.db')
elif DRIVER is None:
    db_uri = f'{DIALECT}+{DRIVER}://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}'
else:
    db_uri = f'{DIALECT}://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}'

SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
