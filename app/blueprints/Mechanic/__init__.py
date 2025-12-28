from flask import Blueprint

mechanics_bp = Blueprint('mechanic',__name__ )
service_tickets_bp = Blueprint('service_tickets', __name__)

from . import routes


