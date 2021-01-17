from flask import Blueprint, redirect, flash, render_template, url_for, request
from travel_planner.models import User, Role
from travel_planner import bcrypt
import datetime
from .forms import RegiserationForm, LoginForm
users = Blueprint('users', __name__)
from flask_login import current_user, login_user, logout_user

# Create users with the three available roles

#  Create 'user@planner.com' user with no roles
if not User.query.filter(User.email == 'user@planner.com').first():
    user = User(
        email='user@planner.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=bcrypt.generate_password_hash('Password1'),
    )
    User.insert(user)

# Create 'manager@planner.com' user with only 'Manager' role
if not User.query.filter(User.email == 'manager@planner.com').first():
    manager = User(
        email='manager@planner.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=bcrypt.generate_password_hash('Password1'),
    )
    user.roles.append(Role(name='Manager'))
    User.insert(manager)

# Create 'admin@planner.com' user with 'Admin' and 'Manager' roles
if not User.query.filter(User.email == 'admin@planner.com').first():
    admin = User(
        email='admin@planner.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=bcrypt.generate_password_hash('Password1'),
    )
    user.roles.append(Role(name='Admin'))
    user.roles.append(Role(name='Manager'))
    User.insert(admin)

@users.route('/register', methods=['POST'])
def register():
    form = RegiserationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    email_confirmed_at=datetime.datetime.utcnow(),
                    password = bcrypt.generate_password_hash(form.password.data),
                    first_name = form.first_name.data,
                    last_name = form.last_name.data)
        User.insert(user)
        flash('User created successfully', 'success')
        return redirect(url_for(user.login))
    return render_template('register.html', form=form, title='Register')

@users.route('login/', methods=['POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).one_or_none()
        if user and bcrypt.check_password_hash(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            return redirect(next or url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Login')

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


