from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customers, db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token
from app import current_app


@customers_bp.route('/', methods=['POST'])
@limiter.limit('5 per hour')
def create_customer():
    data = customer_schema.load(request.json)
    
    new_customer = Customers(**data)
    db.session.add(new_customer)
    db.session.commit()
    
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/login', methods=['POST'])
def login_customer():
    try:
        data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify({e.messages}), 400
    email = data.get('email')
    password = data.get('password')
    
    customer = db.session.execute(
        select(Customers).where(Customers.email == email)
    ).scalar_one_or_none()
    
    if not customer or customer.password != password:
        return jsonify({'error' : 'Invalid credentials'}), 401
    
    token = encode_token(customer.id, current_app.config['SECRET_KEY'])
    
    return jsonify({'token' : token}), 200


@customers_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1 , type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    offset = (page - 1) * per_page
    
    query = (select(Customers).limit(per_page).offset(offset))
    
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({'error' : 'Customer not found'}), 404
    
    return customer_schema.jsonify(customer), 200


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({'error' : 'Customer not found'}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/int:customer_id>', methods=['DELETE'])
@limiter.limit('2 per hour')
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    if not customer:
        return jsonify({'error' : 'Customer not found'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message' : 'Customer account deleted.'}), 200
    
    
    




        


    