from flask import Blueprint, redirect, flash, render_template, url_for, request, jsonify, make_response
from travel_planner.models import User
from travel_planner import bcrypt
import datetime
from .forms import RegiserationForm, LoginForm, UpdateAccountForm, RequestResetForm, PasswordResetForm
from flask_login import login_user, logout_user
from flask_user import roles_required, current_user, login_required
from .utils import save_picture, send_reset_request

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    form = RegiserationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        print('valid')
        user = User(email=form.email.data,
                    email_confirmed_at=datetime.datetime.utcnow(),
                    password=bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8'),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        User.insert(user)
        flash('User created successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        print('valid')
        user = User.query.filter(User.email == form.email.data).one_or_none()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print('logged in')
            next = request.args.get('next')
            return redirect(next or url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('users.login'))
    return render_template('login.html', form=form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data)
            picture_file = save_picture(form.picture.data, current_user.email)
            current_user.picture = picture_file
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        User.update(current_user)
        flash('Account updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form = UpdateAccountForm(obj=current_user)

    image_url = url_for(
        'static', filename='profile_pics/' + current_user.picture)

    return render_template('account.html', form=form, image_url=image_url, title='Account')


@users.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        send_reset_request(user)
        flash('Password reset message was sent to your email', 'info')
        return redirect(url_for('users.login'))

    return render_template('request_reset.html', form=form, title="Forgot password")


@users.route('/reset_token/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetForm()
    user = User.get_reset_token(token)
    if user is None:
        flash('This is an invalid or  expired token', 'warning')
        return redirect('user.reset_password')
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        User.update(user)
        flash('Password changed successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='reset_password')


@users.route('/users')
@roles_required('Manager')
def get_users():
    all_users = User.query.filter(User.email != 'admin@planner.com').all()

    return render_template('users.html', title='All Users', all_users=all_users)


@users.route('/users/<int:user_id>', methods=["POST"])
def edit_user(user_id):
    user = User.query.filter(User.id == user_id).one_or_none
    if user is None:
        return jsonify({
            'success': False,
            'error': 'User does not exist'
        })
    body = request.get_json()
    print(body)
    email = body.get('email', None)
    first_name = body.get('first_name', None)
    last_name = body.get('last_name', None)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.update()
    return jsonify({
        'success': True,
        'updated user': user.id,
    })
