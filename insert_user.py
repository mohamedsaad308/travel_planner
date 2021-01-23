from travel_planner.models import User, Role, UserRoles
import datetime
from travel_planner import bcrypt, db, create_app

app = create_app()
# Create users with the three available roles

#  Create 'user@planner.com' user with no roles
with app.app_context():
    if not User.query.filter(User.email == 'user@planner.com').first():
        user = User(
            email='user@planner.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=bcrypt.generate_password_hash('Password1'),
        )
        db.session.add(user)
        db.session.commit()

    # Create 'manager@planner.com' user with only 'Manager' role
    if not User.query.filter(User.email == 'manager@planner.com').first():
        manager = User(
            email='manager@planner.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=bcrypt.generate_password_hash('Password1'),
        )
        user.roles.append(Role(name='Manager'))
        db.session.add(manager)
        db.session.commit()

    # Create 'admin@planner.com' user with 'Admin' and 'Manager' roles
    if not User.query.filter(User.email == 'admin@planner.com').first():
        admin = User(
            email='admin@planner.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=bcrypt.generate_password_hash('Password1'),
        )
        admin.roles.append(Role(name='Admin'))
        db.session.add(admin)
        db.session.commit()
    # add_role = UserRoles(user_id=3, role_id=1)
    # db.session.add(add_role)
    # db.session.commit()
