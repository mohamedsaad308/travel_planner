from flask_user import roles_required, current_user, login_required
from flask import Blueprint, jsonify, abort, make_response, request
from jwt import encode
from travel_planner.users_api.auth import token_auth
from travel_planner.models import Trip
import datetime
api = Blueprint('trips_api', __name__)

TRIPS_PER_PAGE = 10


def paginate_trips(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * TRIPS_PER_PAGE
    end = start + TRIPS_PER_PAGE
    trips = [trip.format() for trip in selection]
    current_trips = trips[start: end]
    return current_trips


@api.route('/trips')
@roles_required('Admin')
def get_all_trips():
    if not current_user.admin:
        return make_response(jsonify({
            'success': False,
            'error': 'Not Authorized',
        }), 403)
    all_trips = Trip.query.all()
    current_trips = paginate_trips(request, all_trips)
    return jsonify({
        'success': True,
        "trips": current_trips,
        "count": len(all_trips)
    })


@api.route('/trips/<int:trip_id>')
@login_required
def get_one_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Trip not found!',
        }), 404)
    if (current_user.admin) or (current_user.id == trip.trip_user.id):
        return make_response(jsonify({
            'success': True,
            'trip': trip.format(),

        }), 200)
    else:
        abort(403)


@api.route('/trips', methods=['POST'])
@ login_required
def add_trip():
    print('add trip')
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Provide new plan details'
        }), 400)
    destination = body.get('destination', None)
    start_date = body.get('start_date', None)
    end_date = body.get('end_date', None)
    if destination is None or start_date is None or end_date is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Provide new destination, start and end date of your trip'
        }), 400)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print('start date', start_date)
    print('end date', end_date)
    if end_date < start_date:
        return make_response(jsonify({
            'success': False,
            'error': "End date must be after start date!"
        }), 400)
    comment = body.get('comment', None)
    try:
        trip = Trip(destination=destination,
                    start_date=start_date,
                    end_date=end_date,
                    comment=comment,
                    user_id=current_user.id
                    )
        trip.insert()
        return make_response(jsonify({
            'success': True,
            'trip': trip.format(),
        }), 201)
    except BaseException:
        abort(422)


@ api.route('/trips/<int:trip_id>', methods=['PUT'])
@ login_required
def edit_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'trip not found!',
        }), 404)
    if (current_user.admin) or (current_user.id == trip.user_id):
        body = request.get_json()
        if body is None:
            return make_response(jsonify({
                'success': False,
                'error': "Provide information to be editted"
            }), 400)
        destination = body.get('destination', None)
        start_date = body.get('start_date', None)
        end_date = body.get('end_date', None)
        if destination is None or start_date is None or end_date is None:
            return make_response(jsonify({
                'success': False,
                'error': 'Provide new destination, start and end date of your trip'
            }), 400)
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        print('start date', start_date)
        print('end date', end_date)
        if end_date < start_date:
            return make_response(jsonify({
                'success': False,
                'error': "End date must be after start date!"
            }), 400)
        comment = body.get('comment', None)
        try:
            trip.destination = destination
            trip.start_date = start_date
            trip.end_date = end_date
            trip.comment = comment
            trip.update()
            return make_response(jsonify({
                'trip': trip.format(),
                'success': True
            }), 200)
        except:
            abort(422)
    else:
        abort(403)


@ api.route('/trips/<int:trip_id>', methods=['DELETE'])
@ login_required
def delete_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'trip not found!',
        }), 404)
    if (current_user.admin) or (current_user.id == trip.user_id):
        try:
            trip.update()
            return make_response(jsonify({
                'deleted': trip_id,
                'success': True
            }), 200)
        except:
            abort(422)
    else:
        abort(403)

# Get current user trips


@ api.route('/mytrips')
def current_user_trips():
    all_trips = Trip.query.filter(Trip.user_id == current_user.id).all()
    current_trips = paginate_trips(request, all_trips)
    return jsonify({
        'success': True,
        "trips": current_trips,
        "count": len(all_trips)
    })
