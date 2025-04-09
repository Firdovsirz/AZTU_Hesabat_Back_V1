from flask import Blueprint
from models.fealiyyetModel import Fealiyyet
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

fealiyyet_bp = Blueprint('fealiyyet', __name__)

@fealiyyet_bp.route('/api/fealiyyet', methods=['GET'])
def get_fealiyyet():
    try:
        fealiyyets = Fealiyyet.query.all()
        if not fealiyyets:
            return handle_specific_not_found(404, "Fealiyyet not found")
        
        # Convert each Fealiyyet object to a dictionary
        fealiyyet_list = [fealiyyet.fealiyyet_details() for fealiyyet in fealiyyets]
        
        # Return the serialized data as a JSON response
        return handle_success(fealiyyet_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))