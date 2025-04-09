from datetime import datetime
from models.planModel import Plan
from models.userModel import User
from flask import Blueprint, request
from extensions.extensions import db
from models.hesabatModel import Hesabat
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

hesabat_bp = Blueprint('hesabat', __name__)

@hesabat_bp.route('/api/allhesabats', methods=['GET'])
# @token_required
# @role_required([1])
def get_all_hesabat():
    try:
        hesabats = Hesabat.query.all()
        
        if not hesabats:
            return handle_specific_not_found(404, 'No hesabat found.')
        
        hesabat_with_user_data = []
        
        for hesabat in hesabats:
            user = User.query.filter_by(fin_kod=hesabat.fin_kod).first()
    
            if user:
                user_data = user.user_detail()  # Assuming 'user_detail' returns a dictionary of user data
            else:
                user_data = {}

            hesabat_data = {
                "hesabat_id": hesabat.id,
                "hesabat_details": hesabat.hesabat_details(),  # Assuming 'hesabat_details' returns the hesabat details
                "user": user_data
            }
            
            hesabat_with_user_data.append(hesabat_data)
        
        return handle_success(hesabat_with_user_data, "SUCCESS")
    
    except Exception as e:
        return handle_global_exception(str(e))