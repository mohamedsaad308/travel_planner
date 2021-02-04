from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from travel_planner.models import User
from travel_planner.users_api.errors import error_response
from travel_planner import bcrypt
from travel_planner.users_api.errors import error_response

token_auth = HTTPTokenAuth(scheme='Bearer')
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter(User.email == email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
