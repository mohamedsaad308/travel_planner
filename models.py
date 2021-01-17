import datetime
import os
from flask_user import  UserMixin
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from travel_planner import login_manager, db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    active = Column('is_active', Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = Column(String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = Column(DateTime())
    password = Column(String(255), nullable=False, server_default='')

    # User information
    first_name = Column(String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = Column(String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = relationship('Role', secondary='user_roles')
    trips = relationship('Trip', backref='trip_user')

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
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))
#Define the trip data model
class Trip(db.Model):
    __tablename__ = 'trips'
    id = Column(Integer(), primary_key=True)
    destination = Column(String(225), nullable=False)
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    comment = Column(String())
    #Define relationship to the user
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))

    # Trips CRUD methods 
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()





