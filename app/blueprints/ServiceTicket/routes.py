from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, db, Mechanic, Inventory
from . import service_tickets_bp
from app.utils.util import token_required



@service_tickets_bp.post("/")
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    new_ticket = ticket_data  
    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_ticket), 201



@service_tickets_bp.get("/")
def get_service_tickets():
    tickets = db.session.execute(select(ServiceTicket)).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200



@service_tickets_bp.get("/<int:ticket_id>")
def get_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    return service_ticket_schema.jsonify(ticket), 200



@service_tickets_bp.put("/<int:ticket_id>")
def update_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    data = request.json
    if "status" in data:
        ticket.status = data["status"]

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200



@service_tickets_bp.put("/<int:ticket_id>/mechanic")
def assign_mechanic(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    mechanic_id = request.json.get("mechanic_id")
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    ticket.mechanic = mechanic
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200



@service_tickets_bp.put("/<int:ticket_id>/parts")
def update_ticket_parts(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    data = request.json
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    for part_id in add_ids:
        part = db.session.get(Inventory, part_id)
        if part and part not in ticket.parts:
            ticket.parts.append(part)

    for part_id in remove_ids:
        part = db.session.get(Inventory, part_id)
        if part and part in ticket.parts:
            ticket.parts.remove(part)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200



@service_tickets_bp.get("/my-tickets")
@token_required
def my_tickets(customer_id):
    tickets = db.session.execute(
        select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    ).scalars().all()

    return service_tickets_schema.jsonify(tickets), 200






    
    
        
    