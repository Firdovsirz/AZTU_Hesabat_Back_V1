from flask import Blueprint
from models.qiymetlendirmeModel import Qiymetlendirme
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

qiymetlendirme_bp = Blueprint('qiymetlendirme', __name__)

@qiymetlendirme_bp.route('/api/qiymetlendirme', methods=['GET'])
def get_qiymetlendirme():
    try:
        qiymetlendirme = Qiymetlendirme.query.all()
        if not qiymetlendirme:
            return handle_specific_not_found(404, "Qiymetlendirme not found")
        
        qiymetlendirme_details_list = [item.qiymetlendirme_details() for item in qiymetlendirme]
        
        return handle_success(qiymetlendirme_details_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))
    
@qiymetlendirme_bp.route('/api/qiymetlendirme/<int:seviyye_kodu>', methods=['GET'])
def get_qiymetlendirme_by_seviyye_kodu(seviyye_kodu):
    try:
        qiymetlendirme = Qiymetlendirme.query.filter_by(seviyye_kodu=seviyye_kodu).all()
        
        if not qiymetlendirme:
            return handle_specific_not_found(404, "Qiymetlendirme not found.")
        
        qiymetlendirme_details_list = [item.qiymetlendirme_details() for item in qiymetlendirme]
        
        return handle_success(qiymetlendirme_details_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))