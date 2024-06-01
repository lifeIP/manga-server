from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form

from models import Image

from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/1", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html",title="Home")


@app.route("/login/", methods=("GET", "POST"))
def login():
    form = login_form()

    email = form.email.data
    pwd = form.pwd.data
    username = form.username.data
    print(email, pwd, username)
    try:
        user = User.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.pwd, form.pwd.data):
            login_user(user)
            
            resp = jsonify({
                "username": current_user.username,
                "email": current_user.email,
                "message": 'Login success',
                "status": 'success'
            })
            return resp
        else:
            resp = jsonify({
                "message": 'Invalid Username or password!"',
                "status": 'danger'
            })
            return resp
    except Exception as e:
        resp = jsonify({
            "message": 'Invalid Username or password!"',
            "status": 'danger'
        })
        return resp
#admin@flask.ru

# Register route
@app.route("/registration/", methods=("GET", "POST"))
def registration():
    form = register_form()
    try:
        email = form.email.data
        pwd = form.pwd.data
        username = form.username.data
        
        newuser = User(
            username=username,
            email=email,
            pwd=bcrypt.generate_password_hash(pwd),
        )

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    resp = jsonify({
            "response_code": 0,
            "errcode": 0,
            "message": 'Logout success',
            "status": 'success'
        })
    return resp

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
ma=Marshmallow(app)
 
class ImageSchema(ma.Schema):
    class Meta:
        fields = ('id','title')
         
image_schema = ImageSchema(many=True)

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
  
    files = request.files.getlist('files[]')
      
    errors = {}
    success = False
      
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
            newFile = Image(title=filename)
            db.session.add(newFile)
            db.session.commit()
 
            success = True
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
     
@app.route('/images',methods =['GET'])
def images():
    all_images = Image.query.all()
    results = image_schema.dump(all_images)
    return jsonify(results)



if __name__ == "__main__":
    app.run(debug=True)
