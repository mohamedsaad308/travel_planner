from flask import Blueprint, jsonify, abort, make_response, request
from jwt import encode
from travel_planner.users_api.auth import token_auth
from travel_planner.models import Trip
import datetime
api = Blueprint('trips_api', __name__)


@api.route('/trips')
@token_auth.login_required
def get_all_trips():
    if not token_auth.current_user().manager:
        abort(403)
    trips = Trip.query.all()
    return jsonify({
        'success': True,
        "all_trips": [trip.format() for trip in trips]
    })


@api.route('/trips/<int:trip_id>')
@token_auth.login_required
def get_one_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Trip not found!',
        }), 404)
    if (token_auth.current_user().admin) or (token_auth.current_user().id == trip.trip_user.id):
        return make_response(jsonify({
            'success': True,
            'users': trip.format(),

        }), 200)
    else:
        abort(403)


@api.route('/trips', methods=['POST'])
@token_auth.login_required
def add_trip():
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
                    user_id=token_auth.current_user().id
                    )
        trip.insert()
        return make_response(jsonify({
            'success': True,
            'trip': trip.format(),
        }), 201)
    except BaseException:
        abort(422)


@api.route('/trips/<int:trip_id>', methods=['PUT'])
@token_auth.login_required
def edit_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'trip not found!',
        }), 404)
    if (token_auth.current_user().admin) or (token_auth.current_user().id == trip.user_id):
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


@api.route('/trips/<int:trip_id>', methods=['DELETE'])
@token_auth.login_required
def delete_trip(trip_id):
    trip = Trip.query.filter(Trip.id == trip_id).first()
    if trip is None:
        return make_response(jsonify({
            'success': False,
            'error': 'trip not found!',
        }), 404)
    if (token_auth.current_user().admin) or (token_auth.current_user().id == trip.user_id):
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
