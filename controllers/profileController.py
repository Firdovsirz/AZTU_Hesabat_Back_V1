from models.userModel import db, User
from utils.decarator import role_required
from utils.jwt_util import decode_auth_token
from flask import Blueprint, request, jsonify
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_forbidden
from exception.exception import handle_not_found
from exception.exception import handle_unauthorized

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@token_required
@role_required(['SUPERADMIN'])
def profile(user):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return handle_forbidden(403)

    if not auth_header.startswith('Bearer '):
        return jsonify({'message': 'Token format wrong'}), 401

    auth_token = auth_header.split(" ")[1]

    token_data = decode_auth_token(auth_token)

    if not token_data:
        return handle_unauthorized(401, "Inavlid or expired token.")

    user_id = token_data.get('user_id')

    if not user_id:
        return handle_unauthorized(401, "Inavlid or expired token.")

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return handle_not_found(404)
    
    return handle_success(user.user_detail(), "Success")