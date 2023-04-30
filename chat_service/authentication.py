import jwt
from chat_service import config
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2 or auth_headers[0].lower() != 'bearer':
            return jsonify({'error': 'Authorization header is not valid'}), 401

        try:
            token = auth_headers[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
