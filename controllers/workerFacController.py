from models.userModel import User
from flask import Blueprint, request
from models.facultyModel import Faculty
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/api/teacher/<int:faculty_id>', methods=['GET'])
# @token_required
# @role_required(['ADMIN', 'SUPERADMIN'])
def get_workers_by_faculty(faculty_id):
    try:
        # faculty = Faculty.query.filter_by(facultyid=faculty_id).first()
        # if not faculty:
        #     return handle_specific_not_found(404, "Faculty not found.")

        workers = User.query.filter_by(faculty_id=faculty_id).all()
        if not workers:
            return handle_specific_not_found(404, "No workers found for this faculty.")

        result = []
        for worker in workers:
            worker_data = worker.user_detail()
            result.append(worker_data)

        return handle_success(result, "SUCCESS")

    except Exception as e:
        return handle_global_exception(str(e))