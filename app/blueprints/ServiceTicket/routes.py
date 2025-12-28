from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, db, Mechanic
from . import service_tickets_bp

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    query = select(ServiceTicket).where(ServiceTicket.id == ticket_data['id'])

        
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket)

@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found.'}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found.'}), 404
    
    ticket.mechanic = mechanic
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found.'}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found.'}), 404
    
    ticket.mechanic = None
    db.session.commit()
        
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)

@service_tickets_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    
    if ticket:
        return service_ticket_schema.jsonify(ticket), 200
    return jsonify({'error': 'Service ticket not found.'}), 404



    
    
        
    