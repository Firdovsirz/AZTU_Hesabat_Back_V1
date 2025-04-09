import os
import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify
from extensions.extensions import db
from models.facultyModel import Faculty
from models.facultyModel import Kafedra
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

cafedra_bp = Blueprint('cafedra', __name__)
load_dotenv()

@cafedra_bp.route('/api/lms/cafedras', methods=['GET'])
@token_required
@role_required(['ADMIN', 'SUPERADMIN'])
def get_kafedras_from_lms():
    api_url = os.getenv('LMS_API_CAFEDRAS')
    api_key = os.getenv('API_KEY')
    headers = {
        'x-api-key': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        cafedra_data = response.json()

        inserted_count = 0

        for cafedra in cafedra_data:
            existing = Kafedra.query.filter_by(cafedra_code=cafedra['cafedra_code']).first()

            if not existing:
                new_cafedra = Kafedra(
                    cafedra_code=cafedra['cafedra_code'],
                    cafedra_name=cafedra['cafedra_name'],
                    faculty_code=cafedra['faculty_code']
                )
                db.session.add(new_cafedra)
                inserted_count += 1
        if inserted_count > 0:
            db.session.commit()
            return handle_success(cafedra_data, f"{inserted_count} Cafedras fetched and inserted successfully.")
        else:
            return handle_success(cafedra_data, "All cafedras already in the database")
    except Exception as e:
        return handle_global_exception(str(e))
    
@cafedra_bp.route('/api/cafedras', methods=['GET'])
@token_required
@role_required([1, 2])
def get_cafedras():
    try:
        cafedras = Kafedra.query.all()
        if not cafedras:
            return handle_specific_not_found(404, 'Cafedra not found')

        result = []
        for cafedra in cafedras:
            cafedra_data = cafedra.cafedras()
            cafedra_data['faculty_name'] = cafedra.faculty.faculty_name if cafedra.faculty else None
            result.append(cafedra_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}),

@cafedra_bp.route('/api/cafedras/<faculty_code>', methods=['GET'])
@token_required
@role_required([1, 2])
def get_cafedras_by_fac_code(faculty_code):
    try:
        cafedras = Kafedra.query.filter_by(faculty_code=faculty_code).all()
        if not cafedras:
            return handle_specific_not_found(404, 'No cafedras found.')
        cafedra_list = []
        for cafedra in cafedras:
            cafedra_list.append(cafedra.to_dict())
        return handle_success(cafedra_list, "SUCCESS")
    except Exception as e:
        return handle_global_exception(str(e))
