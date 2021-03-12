from flask import Blueprint, render_template


trips = Blueprint('trips', __name__)


@trips.route('/mytrips')
def user_trips():
    return render_template('mytrips.html', title='My Trips')


@trips.route('/trips')
def all_trips():
    return render_template('trips.html', title='Trips')
