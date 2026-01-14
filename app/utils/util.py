from datetime import datetime, timedelta, timezone
from functools import wraps
from jose import jwt, JWTError
from flask import request, jsonify, current_app


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token in missing!'}), 401
        
        try: 
            token = auth_header.split(" ")[1]
            
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            customer_id = payload.get('customer_id')
            if not customer_id:
                return jsonify({'error' : 'Invalid token!'}), 401
        except Exception:
            return jsonify({'error' : 'Token is invali or expired!'}), 401
        
        return f(customer_id, *args, **kwargs)
    return wrapper
        
        

def encode_token(customer_id): 
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1),
        'iat': datetime.now(timezone.utc), 
        'customer_id':  str(customer_id) 
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    
    return token