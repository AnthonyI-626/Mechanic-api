from flask import Blueprint

service_tickets_bp = Blueprint('service_ticket', __name__)

from . import routes