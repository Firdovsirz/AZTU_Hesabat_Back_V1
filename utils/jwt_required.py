from functools import wraps
from flask import request, g
from utils.jwt_util import decode_auth_token
from exception.exception import handle_unauthorized

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return handle_unauthorized(401, 'Authorization token is missing.')

        try:
            token = auth_header.split(" ")[1]
            payload = decode_auth_token(token)

            if payload is None:
                return handle_unauthorized(401, 'Token is invalid or expired.')

            g.user = payload  # Store payload for access in routes

        except Exception as e:
            return handle_unauthorized(401, f'Invalid token format: {str(e)}')

        return f(*args, **kwargs)
    return decorated_function