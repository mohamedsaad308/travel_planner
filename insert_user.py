from travel_planner.models import User, db, Role, UserRoles
import datetime
from travel_planner import bcrypt, create_app

app = create_app()
# Create users with the three available roles

#  Create 'user@planner.com' user with no roles
with app.app_context():
    # User.query.delete()
    # Role.query.delete()
    # UserRoles.query.delete()
    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=app.user_manager.hash_password('Password1'),
        )
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=app.user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Manager'))
        db.session.add(user)
        db.session.commit()
    # create manager@example.com
    if not User.query.filter(User.email == 'manager@example.com').first():
        user = User(
            email='manager@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=app.user_manager.hash_password('Password1'),
        )
        manager = Role.query.filter(Role.name == 'Manager').first()
        db.session.add(user)
        db.session.commit()
        manager_role = UserRoles(user_id=user.id, role_id=manager.id)
        db.session.add(manager_role)
        db.session.commit()

    # add_role = UserRoles(user_id=3, role_id=2)
    # db.session.add(add_role)
    # db.session.commit()
    admin = User.query.filter(User.email == 'member@example.com').first()
    print(len(admin.roles))
    for role in admin.roles:
        print(type(admin.roles))
        print(role.name)
