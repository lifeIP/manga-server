from app import create_app,db,login_manager,bcrypt
from src.database.models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage, UserPhoto, PhotoMask, ModifiedPhoto
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

import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
from PIL import Image


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
    

    
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@my_projects.route("/set_preview_image/<index>", methods=("GET", "POST"))
def set_preview_image(index:int):
    if current_user.is_authenticated:
        project = Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        print(request.files)
        if 'files' not in request.files:
            resp = jsonify({
                "message": 'No file part in the request',
                "status": 'failed'
            })
            resp.status_code = 400
            return resp
        
        files = request.files.getlist('files')
        errors = {}
        success = False
        print(files)

        try:
            os.makedirs("static/upload/" + str(current_user.id) + "/" + str(index))
        except:
            pass

        for file in files:      
            if file and allowed_file(file.filename):
                try:
                    from time import time
                    filename = str(int(time())) + secure_filename(file.filename)
        
                    newpreviewimage = PreviewImage(
                        project_id=index,
                        preview_image_name="static/upload/" + str(current_user.id) + "/" + str(index) + "/" + filename
                    )
                    db.session.add(newpreviewimage)
                    db.session.commit()
                    file.save(os.path.join("static/upload/" + str(current_user.id) + "/" + str(index), filename))
                    success = True
                
                except:
                    success = False
            else:
                resp = jsonify({
                    "message": 'File type is not allowed',
                    "status": 'failed'
                })
                return resp
            
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            errors['status'] = 'failed'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
            resp = jsonify({
                "message": 'Files successfully uploaded',
                "status": 'successs'
            })
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    

@my_projects.route("/get_my_project/<index>", methods=("GET", "POST"))
def get_project(index:int):
    print(request.cookies)
    if current_user.is_authenticated:
        project = Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        preview_image = PreviewImage.query.filter_by(project_id=project.id).first_or_404()
        project_settings = ProjectSettings.query.filter_by(project_id=project.id).first_or_404()

        return jsonify({
            "project_name": project_settings.project_name,
            "project_description": project_settings.project_description,
            "project_status": project_settings.project_status,
            "project_id": project_settings.project_id,
            "preview_image": preview_image.preview_image_name
        })
    else:
        print("Не в аккаунте")
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    

@my_projects.route("/add_user_photos/<index>", methods=("GET", "POST"))
def add_user_photo(index:int):
    if current_user.is_authenticated:
        project = Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        
        if 'files' not in request.files:
            resp = jsonify({
                "message": 'No file part in the request',
                "status": 'failed'
            })
            resp.status_code = 400
            return resp
        
        files = request.files.getlist('files')
        errors = {}
        success = False
        print(files)

        try:
            os.makedirs("static/upload/" + str(current_user.id) + "/" + str(index) + "/original")
        except:
            pass
        
        for file in files:      
            if file and allowed_file(file.filename):
                try:
                    from time import time
                    filename = str(int(time())) + secure_filename(file.filename)
        
                    new_user_photo = UserPhoto(
                        project_id=index,
                        number_in_queue=0,
                        photo_name="static/upload/" + str(current_user.id) + "/" + str(index) + "/original/" + filename
                    )
                    db.session.add(new_user_photo)
                    db.session.commit()
                    file.save(os.path.join("static/upload/" + str(current_user.id) + "/" + str(index) + "/original", filename))
                    success = True
                
                except:
                    success = False
            else:
                resp = jsonify({
                    "message": 'File type is not allowed',
                    "status": 'failed'
                })
                return resp
            
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            errors['status'] = 'failed'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        
        if success:
            resp = jsonify({
                "message": 'Files successfully uploaded',
                "status": 'successs'
            })
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    

@my_projects.route("/get_user_photos/<index>", methods=("GET", "POST"))
def get_user_photos(index:int):
    if current_user.is_authenticated:
        Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        user_photos = UserPhoto.query.filter_by(project_id=index)

        uphoto = []
        for photo in user_photos:
            uphoto.append({"photo_name": photo.photo_name,
                           "number_in_queue": photo.number_in_queue,
                           "project_id": photo.project_id
                           })
        return jsonify(uphoto)
    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    

@my_projects.route("/add_photo_mask/<index>", methods=("GET", "POST"))
def add_photo_mask(index:int):
    if current_user.is_authenticated:
        Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        user_photo = UserPhoto.query.filter_by(project_id=index).first_or_404()

        if 'files' not in request.files:
            resp = jsonify({
                "message": 'No file part in the request',
                "status": 'failed'
            })
            resp.status_code = 400
            return resp
        
        files = request.files.getlist('files')
        errors = {}
        success = False
        print(files)

        try:
            os.makedirs("static/upload/" + str(current_user.id) + "/" + str(index) + "/mask")
        except:
            pass
        
        for file in files:      
            if file and allowed_file(file.filename):
                try:
                    from time import time
                    filename = str(int(time())) + secure_filename(file.filename)
        
                    new_mask = PhotoMask(
                        user_photo_id=user_photo.id,
                        mask_name="static/upload/" + str(current_user.id) + "/" + str(index) + "/mask/" + filename
                    )
                    db.session.add(new_mask)
                    db.session.commit()
                    file.save(os.path.join("static/upload/" + str(current_user.id) + "/" + str(index) + "/mask", filename))
                    success = True
                
                except:
                    success = False
            else:
                resp = jsonify({
                    "message": 'File type is not allowed',
                    "status": 'failed'
                })
                return resp
            
        if success and errors:
            errors['status'] = 'failed'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        
        if success:
            resp = jsonify({
                "message": 'Files successfully uploaded',
                "status": 'successs'
            })
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    
@my_projects.route("/get_mask/<index>", methods=("GET", "POST"))
def get_mask(index:int):
    if current_user.is_authenticated:
        Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        user_photos = UserPhoto.query.filter_by(project_id=index)

        uphoto = []
        for photo in user_photos:
            photo_mask = PhotoMask.query.filter_by(user_photo_id=photo.id).first()
            if(photo_mask != None):
                uphoto.append({"user_photo_id": photo_mask.user_photo_id,
                            "mask_name": photo_mask.mask_name
                            })
        return jsonify(uphoto)
    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })
    
@my_projects.route("/get_modified_photo/<index>", methods=("GET", "POST"))
def get_modified_photo(index:int):
    if current_user.is_authenticated:
        Project.query.filter_by(user_id=current_user.id, id=index).first_or_404()
        user_photos = UserPhoto.query.filter_by(project_id=index)

        uphoto = []
        for photo in user_photos:
            photo = ModifiedPhoto.query.filter_by(user_photo_id=photo.id).first()
            if(photo != None):
                uphoto.append({"user_photo_id": photo.user_photo_id,
                            "mask_name": photo.photo_name
                            })
        return jsonify(uphoto)
    else:
        return jsonify({
            "response_code": 1,
            "errcode": 0,
            "message": 'You are not logged in to your account',
            "status": 'success'
        })