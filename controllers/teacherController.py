from flask import Blueprint
from models.userModel import db, User
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_conflict
from exception.exception import handle_unauthorized
from exception.exception import handle_missing_field
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/api/teachers/<faculty_code>', methods=['GET'])
# @token_required
# @role_required([1, 2])
def get_teacher_by_faculty_code(faculty_code):
    teachers = User.query.filter_by(vezife_id=8, faculty_code=faculty_code).all()
    teacher_list = []
    for teacher in teachers:
        teacher_list.append(teacher.user_detail())
    return handle_success(teacher_list, "SUCCESS")

@teacher_bp.route('/api/teachers/cafedra/<cafedra_code>', methods=['GET'])
@token_required
@role_required([1, 2, 3])
def get_teacher_by_cafedra_code(cafedra_code):
    teachers = User.query.filter_by(vezife_id=8, cafedra_code=cafedra_code).all()
    teacher_list = []
    for teacher in teachers:
        teacher_list.append(teacher.user_detail())
    return handle_success(teacher_list, "SUCCESS")

@teacher_bp.route('/api/teachers', methods=['GET'])
@token_required
@role_required([1])
def get_all_teachers():
    try:
        # Filter users where vezife_id is not null
        teachers = User.query.filter(User.vezife_id != None, User.vezife_id >= 5).all()
        
        if not teachers:
            return handle_specific_not_found(404, 'No teachers found.')
        
        teacher_list = [teacher.user_detail() for teacher in teachers]
        return handle_success(teacher_list, "SUCCESS")
    
    except Exception as e:
        return handle_global_exception(str(e))
    
@teacher_bp.route('/api/execution/teachers', methods=['GET'])
@token_required
@role_required([1])
def get_teacher_by_execution():
    try:
        teachers = User.query.filter_by(ishesabat=1).all()
        if not teachers:
            return handle_specific_not_found(404, 'No teachers found with execution')
        teacher_list =[]
        for teacher in teachers:
            teacher_list.append(teacher.user_detail())
        return handle_success(teacher_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))
    
@teacher_bp.route('/api/execution/teachers/fac/<faculty_code>')
# @token_required
# @role_required([1, 2])
def get_execution_teachers_by_faculty(faculty_code):
    try:
        teachers = User.query.filter_by(faculty_code=faculty_code, ishesabat=1).all()
        if not teachers:
            return handle_specific_not_found(404, 'No teachers found with execution')
        teacher_list =[]
        for teacher in teachers:
            teacher_list.append(teacher.user_detail())
        return handle_success(teacher_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))
    
@teacher_bp.route('/api/execution/teachers/caf/<cafedra_code>')
@token_required
@role_required([1, 2, 3])
def get_execution_teachers_by_cafedra(cafedra_code):
    try:
        teachers = User.query.filter_by(cafedra_code=cafedra_code, ishesabat=1).all()
        if not teachers:
            return handle_specific_not_found(404, 'No teachers found with execution')
        teacher_list =[]
        for teacher in teachers:
            teacher_list.append(teacher.user_detail())
        return handle_success(teacher_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))