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

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/api/allplan', methods=['GET'])
@token_required
@role_required([1])
def get_plan():
    try:
        plans = Plan.query.all()
        
        if not plans:
            return handle_specific_not_found(404, 'No plans found.')
        
        plans_with_user_data = []
        
        for plan in plans:
            user = User.query.filter_by(fin_kod=plan.fin_kod).first()
    
            if user:
                user_data = user.user_detail()
            else:
                user_data = {}

            plan_data = {
                "plan_id": plan.id,
                "plan_details": plan.plan_details(),
                "user": user_data
            }
            
            plans_with_user_data.append(plan_data)
        
        return handle_success(plans_with_user_data, "SUCCESS")
    
    except Exception as e:
        return handle_global_exception(str(e))

@plan_bp.route('/api/plan/<string:fin_kod>', methods=['GET'])
@token_required
@role_required([1, 2, 3])
def get_plan_by_fin_kod(fin_kod):
    try:
        user = User.query.filter_by(fin_kod=fin_kod).first()

        if not user:
            return handle_specific_not_found(404, f"No user found with fin_kod: {fin_kod}")
        
        plans = Plan.query.filter_by(fin_kod=fin_kod).all()

        if not plans:
            return handle_specific_not_found(404, f"No plans found for user with fin_kod: {fin_kod}")
        
        plans_data = [plan.plan_details() for plan in plans]

        response = {
            "user": user.user_detail(),
            "plans": plans_data
        }

        return handle_success(response, "SUCCESS")

    except Exception as e:
        return handle_global_exception(str(e))
@plan_bp.route('/api/create/plan', methods=['POST'])
@token_required
@role_required([1, 2, 3])
def create_plan():
    try:
        data = request.get_json()

        user = User.query.filter_by(fin_kod=data['fin_kod']).first()
        if not user:
            return handle_specific_not_found(404, f"User with fin_kod {data['fin_kod']} not found.")

        last_plan = Plan.query.filter_by(fin_kod=user.fin_kod).order_by(Plan.isin_sira_sayi.desc()).first()
        next_isin_sira_sayi = last_plan.isin_sira_sayi + 1 if last_plan else 1

        # Create new plan
        new_plan = Plan(
            hesabat_ilinin_kodu=datetime.utcnow(),
            bolme_novu_id=data['bolme_novu_id'],
            isin_sira_sayi=next_isin_sira_sayi,
            fealiyyet_novu_id=data['fealiyyet_novu_id'],
            fealiyyet_novu_adi=data['fealiyyet_novu_adi'],
            icra_muddeti=data['icra_muddeti'],
            fin_kod=data['fin_kod']
        )

        # Create a new Hesabat entry as well
        new_hesabat = Hesabat(
            hesabat_ilinin_kodu=datetime.utcnow(),
            bolme_novu_id=data['bolme_novu_id'],
            isin_sira_sayi=next_isin_sira_sayi,
            fealiyyet_novu_id=data['fealiyyet_novu_id'],
            fealiyyet_novu_adi=data['fealiyyet_novu_adi'],
            icra_muddeti=data['icra_muddeti'],
            fin_kod=data['fin_kod']
        )

        user.ishesabat = 1  # Update user's ishesabat status

        # Add the new plan and hesabat to the session
        db.session.add(new_plan)
        db.session.add(new_hesabat)
        db.session.commit()

        return handle_success(new_plan.plan_details(), message="Plan and Hesabat successfully created and user's ishesabat updated.")

    except KeyError as e:
        return handle_global_exception(f"Missing field in request: {str(e)}")

    except Exception as e:
        db.session.rollback()
        return handle_global_exception(str(e))
    

