from app import create_app,db,login_manager,bcrypt
from src.database.models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage
from flask import Blueprint, Flask, json, request, jsonify
from forms import login_form,register_form, create_project_form
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

my_projects = Blueprint('my_projects', __name__, template_folder='templates')

@my_projects.route("/create_my_project/", methods=("GET", "POST"))
def create_project():
    form = create_project_form()
    try:
        print(form.data)
        if current_user.is_authenticated:
            
            newproject = Project(
                user_id = current_user.id
            )
            
            newproject_settings = ProjectSettings(
                project_name=form.project_name.data
            )
            
            newproject.project_settings.append(newproject_settings)
            db.session.add(newproject)
            db.session.commit()


            print("/projects/ ", current_user.id)
            return jsonify({
                "response_code": 0,
                "errcode": 0,
                "message": 'All ok',
                "status": 'success'
            })
        else:
            return jsonify({
                "response_code": 1,
                "errcode": 0,
                "message": 'You are not logged in to your account',
                "status": 'success'
            })
    except:
        print("error")
        return jsonify({
            "response_code": -1,
            "errcode": -1,
            "message": 'error',
            "status": 'Suka, KUDA LEZESH'
        })
