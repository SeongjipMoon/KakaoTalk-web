import os


# session secret
SECRET_KEY = 'secret'

CLIENT_ID = os.environ['CLIENT_ID']
REDIRECT_URL = os.environ['REDIRECT_URL']

MONGO_DBNAME = os.environ['DATABASE']
MONGO_URI = 'mongodb://{}:{}/{}'. format(
    os.environ['DATABASE_SERVER'],
    os.environ['DATABASE_PORT'],
    os.environ['DATABASE']
)