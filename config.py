import os

from local_settings import SECRET_PASSWORD

class Config:
    SECRET_PASSWORD = SECRET_PASSWORD
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "el_pepe_123"

class DevelopmentConfig(Config):
    DEGUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
    }