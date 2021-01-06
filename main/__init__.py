import Flask
from planner.config import Config
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy

def create_app(config_class=Config):
    app = Flask(__name__)
    babel = Babel(app)
    db = SQLAlchemy(app)
    user_manager = UserManager(app, db, User)