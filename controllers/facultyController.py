import os
import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify
from extensions.extensions import db
from models.facultyModel import Faculty
from utils.decarator import role_required
from utils.jwt_required import token_required
from exception.exception import handle_success
from exception.exception import handle_global_exception
from exception.exception import handle_specific_not_found

faculty_bp = Blueprint('faculty', __name__)
load_dotenv()

@faculty_bp.route('/api/lms/faculties', methods=['POST'])
# @token_required
# @role_required(['ADMIN', 'SUPERADMIN'])
def get_faculties_from_lms():
    api_url = os.getenv('LMS_API_FACULTIES')
    api_key = os.getenv('API_KEY')
    headers = {
        'x-api-key': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        faculty_data = response.json()

        inserted_count = 0

        for faculty in faculty_data:
            existing = Faculty.query.filter_by(faculty_code=faculty['faculty_code']).first()

            if not existing:
                new_faculty = Faculty(
                    faculty_code=faculty['faculty_code'],
                    faculty_name=faculty['faculty_name']
                )
                db.session.add(new_faculty)
                inserted_count += 1

        if inserted_count > 0:
            db.session.commit()
            return handle_success(faculty_data, f"{inserted_count} Faculties fetched and inserted successfully.")
        else:
            return handle_success(faculty_data, "All faculties are already in the database. No new entries.")

    except Exception as e:
        return handle_global_exception(str(e))


@faculty_bp.route('/api/faculties', methods=['GET'])
@token_required
@role_required([1])
def get_all_faculties_with_kafedras():
    try:
        faculties = Faculty.query.all()
        if not faculties:
            return handle_specific_not_found(404, "Faculty not found.")

        result = []
        for faculty in faculties:
            faculty_data = faculty.to_dict()  # Using to_dict method to get a dictionary
            kafedra_data = [kafedra.to_dict() for kafedra in faculty.kafedras]  # Serialize kafedras
            faculty_data['kafedras'] = kafedra_data
            result.append(faculty_data)

        return handle_success(result, "SUCCESS")

    except Exception as e:
        return handle_global_exception(str(e))