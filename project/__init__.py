from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import secure_filename
import os


# init SQLAlchemy to use it later
db = SQLAlchemy()

# create media route to store files
UPLOAD_FOLDER = ""
if os.name == "posix":
    # media root in linux
    UPLOAD_FOLDER = "/opt/SGDF"
elif os.name == "nt":
    # media root in windows
    UPLOAD_FOLDER = "C:\SGDF"
else:
    # default folder in other os is the current route
    UPLOAD_FOLDER = os.getcwd()

# configures the app

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'djubdrREuibuBireJberKobnSrEFcfgDG'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
