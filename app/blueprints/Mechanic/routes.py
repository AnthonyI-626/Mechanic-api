from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp



@mechanics_bp.route("/mechanics", methods=['POST'])
def create_customer():
    try:
        mechanic_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': 'Email already associated with account'}), 400
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    
    existing_customer = db. session.execute(query).scalars().all()
    
    new_customer = Mechanic(**mechanic_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)
@mechanics_bp.route("/mechanics", methods = ['GET'])
def get_customers():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return customer_schema.jsonify(mechanics)

@mechanics_bp.route('/mechanics/<int:customer_id>', methods = ['GET'])
def get_customer(customer_id):
    mechanic = db.session.get(Mechanic, customer_id)
    
    if mechanic:
        return customer_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404
@mechanics_bp.route('/mechanics/<int:customer_id>', methods = ['PUT'])
def update_customer(customer_id):
    mechanic = db.session.get(Mechanic, customer_id)
    
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(mechanic), 200

@mechanics_bp.route('/mechanic/<int:customer_id>', methods = ['DELETE'])
def delete_customer(customer_id):
    mechanic = db.session.get(Mechanic, customer_id)
    
    if not mechanic:
        return jsonify({"error": 'Mechanic not found'}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message' : f'Mechanic id: {customer_id}, successfully deleted.'}), 200