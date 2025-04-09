from flask import Flask
from flask_cors import CORS
from config.config import Config
from extensions.extensions import db
from controllers.authController import auth_bp
from controllers.planController import plan_bp
from controllers.roleController import role_bp
from controllers.pagesController import pages_bp
from controllers.cafedraController import cafedra_bp
from controllers.hesabatController import hesabat_bp
from controllers.profileController import profile_bp
from controllers.facultyController import faculty_bp
from controllers.teacherController import teacher_bp
from controllers.workerFacController import worker_bp
from controllers.fealiyyetController import fealiyyet_bp
from controllers.qiymetlendirmeController import qiymetlendirme_bp

def main_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(fealiyyet_bp)
    app.register_blueprint(qiymetlendirme_bp)
    app.register_blueprint(cafedra_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(hesabat_bp)

    return app

if __name__ == '__main__':
    app = main_app()
    app.run(debug=True)