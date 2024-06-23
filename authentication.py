from app import create_app,db,login_manager,bcrypt
from models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage, PhotosFromTheFeed, PhotoMask
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

my_auth = Blueprint('my_auth', __name__, template_folder='templates')


@my_auth.route("/login/", methods=("GET", "POST"))
def login():
    form = login_form()
    print(form.data)
    try:
        print("user")
        user = UserSettings.query.filter_by(email=form.email.data).first()
        print("user")
        if check_password_hash(user.pwd, form.pwd.data):

            print("check_password_hash")
            login_user(User.query.get(int(user.user_id)))
            print("login_user")

            resp = jsonify({
                "response_code": 0,
                "errcode": 0,
                "message": 'Login success',
                "status": 'success'
            })
            return resp
        else:
            resp = jsonify({
                "response_code": 1,
                "errcode": -1,
                "message": 'Invalid Username or password!"',
                "status": 'danger'
            })
            return resp
    except Exception as e:
        resp = jsonify({
            "response_code": 2,
            "errcode": -1,
            "message": 'Invalid Username or password!"',
            "status": 'danger'
        })
        return resp
#admin@flask.ru

# Register route
@my_auth.route("/registration/", methods=("GET", "POST"))
def registration():
    form = register_form()
    print(form.data)
    try:
        newuser = User(
        )
        
        newuser_settings = UserSettings(
            user_name=form.username.data,
            email=form.email.data,
            pwd=bcrypt.generate_password_hash(form.pwd.data)
        )
        
        site_settings = SiteSettings()

        newuser.user_settings.append(newuser_settings)
        newuser.site_settings.append(site_settings)
        db.session.add(newuser)
        db.session.commit()
        
        resp = jsonify({
                "response_code": 0,
                "errcode": 0,
                "message": 'Account Succesfully created',
                "status": 'success'
            })
        return resp

    except InvalidRequestError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 1,
            "errcode": -1,
            "message": 'Something went wrong!',
            "status": 'danger'
        })
        return resp
    except IntegrityError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 2,
            "errcode": 1,
            "message": 'User already exists!',
            "status": 'warning'
        })
        return resp
    except DataError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 3,
            "errcode": 1,
            "message": 'Invalid Entry',
            "status": 'warning'
        })
        return resp
    except InterfaceError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 4,
            "errcode": -1,
            "message": 'Error connecting to the database',
            "status": 'danger'
        })
        return resp
    except DatabaseError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 5,
            "errcode": -1,
            "message": 'Error connecting to the database',
            "status": 'danger'
        })
        return resp
    except BuildError:
        db.session.rollback()
        resp = jsonify({
            "response_code": 6,
            "errcode": -1,
            "message": 'An error occured!',
            "status": 'danger'
        })
        return resp

