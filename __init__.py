from flask import Flask
from travel_planner.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
# from flask_user import UserManager
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app. config.from_object(Config)
    babel = Babel(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from travel_planner.main.routes import main
    from travel_planner.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)
    return app
from travel_planner.models import User
# user_manager = UserManager(create_app(), db, User)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#To create the database
# db.create_all(app=create_app())