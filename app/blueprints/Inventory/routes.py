from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Inventory
from . import inventory_bp


@inventory_bp.route('/', methods=['POST'])
def create_inventory_item():
    data = inventory_schema.load(request.json)
    
    new_item = Inventory(**data)
    db.session.add(new_item)
    db.session.commit()
    
    return inventory_schema.jsonify(new_item), 201

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    query = select(Inventory)
    items = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(items), 200

@inventory_bp.route('/<int:item_id>', methods=["GET"])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error' : 'Item not found'}), 404
    
    return inventory_schema.jsonify(item), 200


@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error' : 'Item not found'}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(item, key, value)
        
    db.session.commit()
    return inventory_schema.jsonify(item), 200


@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    if not item:
        return jsonify({'error' : 'item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message' : 'Item deleted.'}), 200