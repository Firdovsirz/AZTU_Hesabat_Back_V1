from flask_cors import cross_origin
from flask import Blueprint, request
from models.userModel import db, User
from utils.jwt_util import encode_auth_token
from exception.exception import handle_creation
from exception.exception import handle_conflict
from exception.exception import handle_not_found
from exception.exception import handle_unauthorized
from exception.exception import handle_missing_field
from exception.exception import handle_signin_success

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    required_fields = [
        'ad', 'soyad', 'ata_adi', 'fin_kod', 'password', 'faculty_code',
        'cafedra_code', 'vezife_id',
        'vezife_name', 'ishesabat', 'role_code'
    ]

    for field in required_fields:
        if field not in data:
            return handle_missing_field(404)
        
    ad = data.get('ad')
    soyad = data.get('soyad')
    ata_adi = data.get('ata_adi')
    fin_kod = data.get('fin_kod')
    password = data.get('password')
    faculty_code = data.get('faculty_code')
    cafedra_code = data.get('cafedra_code')
    vezife_id = data.get('vezife_id')
    vezife_name = data.get('vezife_name')
    ishesabat = data.get('ishesabat')
    role_code = data.get('role_code')

    if User.query.filter_by(fin_kod=fin_kod).first():
        return handle_conflict(409)


    user = User(
        ad=ad,
        soyad=soyad,
        ata_adi=ata_adi,
        fin_kod=fin_kod,
        password_hash='',
        faculty_code=faculty_code,
        cafedra_code=cafedra_code,
        vezife_id=vezife_id,
        vezife_name=vezife_name,
        ishesabat=ishesabat,
        role_code=role_code
    )
    
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return handle_creation("User registered successfully.")

@auth_bp.route('/api/signin', methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
def signin():
    data = request.get_json()
    fin_kod = data.get('fin_kod')
    password = data.get('password')

    user = User.query.filter_by(fin_kod=fin_kod).first()

    if not user:
        return handle_unauthorized(401, "Invalid credentials.")
    
    if not user.check_password(password):
        return handle_unauthorized(401, "Invalid credentials.")
    
    token = encode_auth_token(user.id, user.fin_kod)

    return handle_signin_success(user.user_detail(), "Login granted.", token)