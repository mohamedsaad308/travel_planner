import time
import os
from flask_user import UserMixin
from travel_planner import db, login_manager
import jwt

from dotenv import load_dotenv

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'),
                      nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    picture = db.Column(db.String(255), nullable=False, default='picture.png')
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'),
                           nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'),
                          nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')
    trips = db.relationship('Trip', backref='trip_user')

    def set_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.email, 'exp': time.time() + expires}, key=os.getenv('SECRET_KEY'))

    @staticmethod
    def get_reset_token(token):
        try:
            email = jwt.decode(token, key=os.getenv('SECRET_KEY'))[
                'reset_password']

        except Exception as e:
            print(e)
            return
        return User.query.filter(User.email == email).first()

    def __repr__(self):
        return f"{self.email}, {self.picture}"

    # User CRUD methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))
# Define the trip data model


class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer(), primary_key=True)
    destination = db.Column(db.String(225), nullable=False)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    comment = db.Column(db.String())
    # Define relationship to the user
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))

    # Trips CRUD methods
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
