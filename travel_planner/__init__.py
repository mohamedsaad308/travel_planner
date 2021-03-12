import datetime
from flask import Flask
from travel_planner.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_user import UserManager
from flask_migrate import Migrate
import os
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    babel = Babel(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    mail.init_app(app)
    csrf = CSRFProtect(app)
    migrate.init_app(app, db)
    from travel_planner.main.routes import main
    from travel_planner.users.routes import users
    from travel_planner.trips.routes import trips
    from travel_planner.users_api.users import api as api_bp
    from travel_planner.trips_api.routes import api as trips_api

    app.register_blueprint(main)
    app.register_blueprint(trips)
    app.register_blueprint(users)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(trips_api, url_prefix='/api')
    # Setup Flask-User
    from .models import User, Role
    user_manager = UserManager(app, db, User)
    login_manager.login_view = 'users.login'

    return app


# db.create_all(app=create_app())


#     db.drop_all(app=create_app())
#     db.create_all(app=create_app())


# to rebuild database
# db_drop_and_create_all()
