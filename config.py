import os
from dotenv import load_dotenv
load_dotenv()



class Config:
    """ Flask application config """

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Flask-SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    #Define database path

    database_filename = "database.db"
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = "sqlite:///{}".format(
        os.path.join(project_dir, database_filename))
    SQLALCHEMY_DATABASE_URI = database_path
    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"