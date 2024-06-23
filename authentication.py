from app import create_app,db,login_manager,bcrypt
from models import User, UserSettings, SiteSettings, Project, ProjectSettings, PreviewImage, PhotosFromTheFeed, PhotoMask
from routes import app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))