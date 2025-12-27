from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp



@customers_bp.route("/customers", methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': 'Email already associated with account'}), 400
    query = select(Customer).where(Customer.email == customer_data['email'])
    
    existing_customer = db. session.execute(query).scalars().all()
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)
customers_bp.route("/customers", methods = ['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customer_schema.jsonify(customers)

@app.route('/customers/<int:customer_id>', method = ['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

app.route('/customers/<int:customer_id>', methods = ['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200

app.route('/customer/<int: customer_id>', methods = ['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": 'Customer not found'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message' : f'Customer id: {customer_id}, successfully deleted.'}), 200