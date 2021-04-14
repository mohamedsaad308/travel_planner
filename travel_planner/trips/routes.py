from flask import Blueprint, render_template
from flask_user import roles_required, login_required

trips = Blueprint('trips', __name__)


@trips.route('/mytrips')
@login_required
def user_trips():
    return render_template('mytrips.html', title='My Trips')


@trips.route('/trips')
@roles_required('Admin')
def all_trips():
    return render_template('trips.html', title='Trips')
