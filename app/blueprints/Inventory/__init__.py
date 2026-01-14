from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)
service_ticket_bp = Blueprint('service_ticket', __name__)

from . import routes