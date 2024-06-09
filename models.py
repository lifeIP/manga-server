from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_pwd
    

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30), unique=False, nullable=False)
    description = db.Column(db.String(1200), unique=False, nullable=False)


class Image(db.Model):
    __tablename__ = "images"
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.String(120), unique=True, nullable=False)
    number_in_queue = db.Column(db.Integer, unique=False, nullable=False)