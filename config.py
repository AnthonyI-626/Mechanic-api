class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:J101310112408e!@localhost/mechanic_api'
    DEBUG = True
    
    
class TestingConfig:
    pass

class ProductionConfig:
    pass