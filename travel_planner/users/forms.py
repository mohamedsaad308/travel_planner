from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from travel_planner.models import User
from flask_login import current_user


class RegiserationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    cofirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign up')
    def validate_email(self, email):
        if User.query.filter(User.email == email.data).first():
            raise ValidationError("This email is alread registered!")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update account')
    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter(User.email == email.data).first():
                raise ValidationError("This email is alread registered!")

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')
    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).one_or_none()
        if user is None:
            raise ValidationError("This email is not registered!")
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    cofirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Change Password')