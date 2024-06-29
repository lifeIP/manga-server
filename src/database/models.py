from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    user_settings = db.relationship('UserSettings', backref='user')
    site_settings = db.relationship('SiteSettings', backref='user')

class UserSettings(db.Model):
    __tablename__ = "user_settings"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(15), unique=False, nullable=False, default="No Name")
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), unique=True, nullable=False)

class SiteSettings(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    theme = db.Column(db.Boolean, default=1)

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    project_settings = db.relationship("ProjectSettings", backref="project")
    preview_image = db.relationship("PreviewImage", backref="project")
    user_photo = db.relationship("UserPhoto", backref="project")

class ProjectSettings(db.Model):
    __tablename__ = "project_settings"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project_name = db.Column(db.String(50), unique=False, nullable=False, default="Нет названия")
    project_description = db.Column(db.Text(1200), unique=False, default="Нет описания")
    project_status = db.Column(db.Integer, default=0)

class PreviewImage(db.Model):
    __tablename__ = "preview_image"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), unique=True)
    preview_image_name = db.Column(db.String(50), unique=False, nullable=False, default="0.png")
    
class UserPhoto(db.Model):
    __tablename__ = "user_photo"
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    number_in_queue = db.Column(db.Integer, unique=False, nullable=False)
    photo_name = db.Column(db.String(30), unique=False, nullable=False, default="0.png")

    modified_photo = db.relationship("ModifiedPhoto", backref="user_photo")
    photo_mask = db.relationship("PhotoMask", backref="user_photo")


class ModifiedPhoto(db.Model):
    __tablename__ = "modified_photo"

    id = db.Column(db.Integer, primary_key=True)
    user_photo_id = db.Column(db.Integer, db.ForeignKey('user_photo.id'))


class PhotoMask(db.Model):
    __tablename__ = "photo_mask"
    
    id = db.Column(db.Integer, primary_key=True)
    user_photo_id = db.Column(db.Integer, db.ForeignKey('user_photo.id'))
    mask_name = db.Column(db.String(30), unique=False, nullable=False, default="0.png")
    status = db.Column(db.Integer, unique=False, nullable=False, default=0)