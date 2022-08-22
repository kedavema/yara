class Config:
    """ General configuration parent clas"""
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {"development" : DevelopmentConfig}