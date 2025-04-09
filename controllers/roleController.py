from models.userModel import User
from models.roleModel import Roles
from flask import Blueprint, request
from extensions.extensions import db
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

role_bp = Blueprint('roles', __name__)


@role_bp.route('/api/update/role', methods=['PUT'])
@token_required
@role_required(['SUPERADMIN'])
def update_role():
    try:
        data = request.get_json()
        fin_kod = data.get('fin_kod')
        new_role_code = data.get('role_code')

        user = User.query.filter_by(fin_kod=fin_kod).first()
        if not user:
            return handle_specific_not_found(404, 'User not found.')
        
        # Check if the new role_code is the same as the current one
        if user.role_code == new_role_code:
            return handle_specific_not_found(404, 'The new role_code is the same as the current one.')
        
        user.role_code = new_role_code
        db.session.commit()
        
        return handle_success(user.user_detail(), "User role updated successfully.")
    except Exception as e:
        return handle_global_exception(str(e))