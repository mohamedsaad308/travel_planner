import sys
import uuid
from flask import Blueprint, request, jsonify, make_response, abort
from travel_planner.models import User
from travel_planner import bcrypt
import datetime
import re
from travel_planner.users_api.auth import token_auth
from travel_planner.users_api.auth import basic_auth
from flask import Blueprint
from flask_user import roles_required, current_user, login_required
api = Blueprint('users_api', __name__)


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


# For pagination purpose
USERS_PER_PAGE = 10


def paginate_users(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE
    users = [user.short() for user in selection]
    current_users = users[start: end]
    return current_users


@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    # print(token, type(token))
    # access_token = json.dumps({'token': token})
    return jsonify({'token': token})


@api.route('/users')
@roles_required(['Manager', 'Admin'])
def get_users():
    # if not token_auth.current_user().manager:
    #     abort(403)
    # Return all users except for admin
    all_users = User.query.filter(User.email != 'admin@example.com').all()
    current_users = paginate_users(request, all_users)
    return make_response(jsonify({
        'success': True,
        'users': current_users,
        'count': len(all_users)

    }), 200)


@ api.route('/users-detail')
@roles_required(['Manager', 'Admin'])
def get_users_detail():
    # if not token_auth.current_user().manager:
    #     abort(403)
    # Return all users except for admin
    all_users = User.query.filter(User.email != 'admin@example.com').all()
    users_dict = [user.long() for user in all_users]
    return make_response(jsonify({
        'success': True,
        'users': users_dict,
        'count': len(all_users)

    }), 200)


@ api.route('/users/<int:user_id>')
@ token_auth.login_required
def get_one_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return make_response(jsonify({
            'success': False,
            'error': 'User not found!',
        }), 404)
    # don't allow getting admin details
    if user.email == 'admin@example.com':
        abort(403)
    if (token_auth.current_user().manager) or (token_auth.current_user().id == user.id):
        return make_response(jsonify({
            'success': True,
            'users': user.long(),

        }), 200)
    else:
        abort(403)


@ api.route('/users/search', methods=['POST'])
@roles_required(['Manager', 'Admin'])
def search_users():
    if not current_user.manager:
        abort(403)
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Provide valid search word'
        }), 400)
    search = body.get('search', None)
    result = User.query.filter(
        User.email.ilike(f'%{search}%'), User.email != 'admin@example.com').order_by(
        User.id).all()
    current_users = paginate_users(request, result)
    return make_response(jsonify({
        'success': True,
        'users': current_users,
        'count': len(result)

    }), 200)


@ api.route('/users', methods=['POST'])
@roles_required(['Manager', 'Admin'])
def create_user():
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Provide new user details or search information'
        }), 400)
    if 'search' in body:
        search = body.get('search', None)
        result = User.query.filter(
            User.email.ilike(f'%{search}%'), User.email != 'admin@example.com').order_by(
            User.id).all()
        current_users = paginate_users(request, result)
        return make_response(jsonify({
            'success': True,
            'users': current_users,
            'count': len(result)

        }), 200)
    email = body.get('email', None)
    password = body.get('password', None)
    if (not email) or (not password):
        return make_response(jsonify({
            'success': False,
            'error': 'You did not provide email and password'
        }), 400)
    if not valid_email(email):
        return make_response(jsonify({
            'success': False,
            'error': 'This is not a valid email'
        }), 400)
    registered_user = User.query.filter(User.email == email).one_or_none()
    if registered_user:
        return make_response(jsonify({
            'success': False,
            'error': 'Email already registered'
        }), 400)
    try:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=email,
            password=bcrypt.generate_password_hash(
                password).decode('utf-8'),
            email_confirmed_at=datetime.datetime.utcnow(),
            first_name=body.get('first_name', None),
            last_name=body.get('last_name', None)
        )
        new_user.insert()
        all_users = User.query.filter(User.email != 'admin@example.com').all()
        current_users = paginate_users(request, all_users)
        return jsonify({
            'success': True,
            'users': current_users,
            'count': len(all_users),
            'created': new_user.short(),
            'token': new_user.get_token()
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)


@api.route('/users/<int:user_id>', methods=["PATCH"])
@login_required
def edit_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return make_response(jsonify({
            'success': False,
            'error': 'User not found!',
        }), 404)
    # don't allow getting admin details
    if user.email == 'admin@example.com':
        abort(403)
    if (current_user.manager) or (current_user.id == user.id):
        try:
            body = request.get_json()
            if body is None:
                return make_response(jsonify({
                    'success': False,
                    'error': 'Provide edited user information'
                }), 400)
            email = body.get('email', None)
            if email:
                if valid_email(email):
                    existing_user = User.query.filter(
                        User.email == email).first()
                    if existing_user and email != user.email:
                        return make_response(jsonify({
                            'success': False,
                            'error': "Email is already registered"
                        }), 400)
                    else:
                        user.email = email
                else:
                    return make_response(jsonify({
                        'success': False,
                        'error': "Email is not well formatted"
                    }), 400)
            first_name = body.get('first_name', None)
            last_name = body.get('last_name', None)
            password = body.get('password', None)
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if password:
                user.password = bcrypt.generate_password_hash(
                    password).decode('utf-8')
            user.update()
            return jsonify({
                'success': True,
                'updated': user.short(),
            })
        except BaseException:
            print(sys.exc_info())
            abort(422)
    else:
        abort(403)


@ api.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.manager:
        abort(403)
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return make_response(jsonify({
            'success': False,
            'error': 'User does not exist'
        }), 404)
    try:
        user.delete()
        all_users = User.query.filter(User.email != 'admin@example.com').all()
        current_users = paginate_users(request, all_users)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'users': current_users,
            'count': len(all_users)
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)


@ api.route('/users/<int:user_id>/promote', methods=['PATCH'])
@ token_auth.login_required
def promote_user(user_id):
    if not token_auth.current_user().admin:
        abort(403)
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return make_response(jsonify({
            'success': False,
            'error': 'User does not exist'
        }), 404)
    body = request.get_json()
    if body is None:
        abort(400)
    is_admin = body.get('is_admin', None)
    is_manager = body.get('is_manager', None)
    if is_admin is None and is_manager is None:
        abort(400)
    try:
        if is_admin != None:
            user.admin = is_admin
        if is_manager != None:
            user.manager = is_manager
        # print(is_manager, is_admin)
        user.update()
        return jsonify({
            'success': True,
            'promoted_user': user.long()
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)
