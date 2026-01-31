import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:J101310112408e!@localhost/mechanic_api'
    DEBUG = True
    
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    SECRET_KEY = 'test-secret-key'



