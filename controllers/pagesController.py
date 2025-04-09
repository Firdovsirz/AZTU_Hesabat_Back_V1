from datetime import datetime
from models.pagesModel import Pages
from extensions.extensions import db
from flask import Blueprint, request, g
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/api/pages', methods=['GET'])
@token_required
@role_required([4])
def get_pages():
    try:
        pages = Pages.query.all()
        page_list = [page.page_details() for page in pages]
        return handle_success(page_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))

@pages_bp.route('/api/pages/role-code')
@token_required
@role_required([1, 2, 3, 4])
def get_pages_role_code():
    try:
        role_code = g.user['role_code']
        pages = Pages.query.filter_by(role_code=role_code).all()
        pages_data = [page.page_details() for page in pages]
        return handle_success(pages_data, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))