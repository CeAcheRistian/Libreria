class Config:
    pass

class DevelopmentConfig(Config):
    DEGUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
    }