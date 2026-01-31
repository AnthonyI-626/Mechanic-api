from flask import Flask
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.Mechanic import mechanics_bp
from .blueprints.ServiceTicket import service_tickets_bp
from .blueprints.Customers import customers_bp
from .blueprints.Inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.yaml'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Service API"
    }
)

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name is None: 
      config_name = 'TestingConfig'
        
    app.config.from_object(f'config.{config_name}')
    
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    from .models import Customers, Mechanic, ServiceTicket, Inventory

    return app