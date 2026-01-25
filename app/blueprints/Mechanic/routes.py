from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.models import Mechanic, db, ServiceTicket
from . import mechanics_bp
from app.extensions import limiter, cache



@mechanics_bp.route("/", methods=['POST'])
@limiter.limit('3 per hour')
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400

    existing = db.session.execute(
        select(Mechanic).where(Mechanic.email == mechanic_data["email"])
    ).scalar_one_or_none()

    if existing:
        return jsonify({"error": "Email already associated with an account"}), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201





@mechanics_bp.route("/", methods = ['GET'])
@cache.cached(timeout=60)
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:mechanic_id>', methods = ['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404


@mechanics_bp.route('/<int:mechanic_id>', methods = ['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:mechanic_id>', methods = ['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": 'Mechanic not found'}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message' : f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200


@mechanics_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    results = (db.session.query(Mechanic).outerjoin(Mechanic.tickets).group_by(Mechanic.id).order_by(func.count(ServiceTicket.id).desc()).all())
    
    return mechanics_schema.jsonify(results), 200