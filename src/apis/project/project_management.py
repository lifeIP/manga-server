from flask_login import current_user
from src.database.models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage
from flask import Blueprint, Flask, abort, json, request, jsonify, redirect, url_for


my_projects = Blueprint('my_projects', __name__, template_folder='templates')

@my_projects.route("/projects/")
def get_project():
    if current_user.is_authenticated:
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