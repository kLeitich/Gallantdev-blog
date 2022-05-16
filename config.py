import os

class Config:
    SECRET_KEY = 'voke'
    SQLALCHEMY_TRACK_MODIFICATION = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1421@localhost/blog'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
     # api config
    QOUTE_API_URL='http://quotes.stormconsultancy.co.uk/random.json'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1421@localhost/blog'
    QOUTE_API_URL='http://quotes.stormconsultancy.co.uk/random.json'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",)

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}