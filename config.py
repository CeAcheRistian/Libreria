import os

from decouple import config

from local_settings import SECRET_PASSWORD

class Config:
    SECRET_PASSWORD = SECRET_PASSWORD
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "el_pepe_123"

class DevelopmentConfig(Config):
    DEGUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL')
    MAIL_PASSWORD = config('MAIL_PASSWORD')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
    }