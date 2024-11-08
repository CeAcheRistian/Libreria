from local_settings import SECRET_PASSWORD

class Config:
    SECRET_PASSWORD = SECRET_PASSWORD

class DevelopmentConfig(Config):
    DEGUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
    }