from flask_user import roles_required, current_user, login_required
from flask import Blueprint, jsonify, abort, make_response, request
from jwt import encode
from travel_planner.users_api.auth import token_auth
from travel_planner.models import Trip
import datetime
from sqlalchemy import text, desc, asc
api = Blueprint('trips_api', __name__)

TRIPS_PER_PAGE = 10


def get_offset(request):
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * TRIPS_PER_PAGE
    return offset


@api.route('/trips')
@roles_required('Admin')
def get_all_trips():
    if not current_user.admin:
        return make_response(jsonify({
            'success': False,
            'error': 'Not Authorized',
        }), 403)

    offset = get_offset(request)
    all_trips_count = Trip.query.count()
    current_trips = Trip.query.order_by(
        text('id')).offset(offset).limit(TRIPS_PER_PAGE)
    return jsonify({
        'success': True,
        "trips": [trip.format() for trip in current_trips],
        "count": all_trips_count
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
    # print('add trip')
    body = request.get_json()
    if body is None:
        return make_response(jsonify({
            'success': False,
            'error': 'Provide new plan details'
        }), 400)
    if 'search' in body:
        offset = get_offset(request)
        order_by = body.get('order_by', None)
        search = body.get('search', None)
        order_type = body.get('order_type', None)
        from_date = body.get('from_date', None)
        to_date = body.get('to_date', None)
        if from_date and to_date:
            from_to = from_date <= Trip.start_date <= to_date
        elif from_date:
            from_to = Trip.start_date >= from_date
        elif to_date:
            from_to = Trip.start_date <= to_date
        else:
            from_to = True
        direction = desc if order_type == 'desc' else asc
        if current_user.admin:
            count = Trip.query.filter(
                Trip.destination.ilike(f'%{search}%'), from_to).count()
            current_trips = Trip.query.filter(
                Trip.destination.ilike(f'%{search}%'), from_to).order_by(direction
                                                                         (text(order_by))).offset(offset).limit(TRIPS_PER_PAGE)
        else:
            count = Trip.query.filter(
                Trip.destination.ilike(f'%{search}%'), Trip.user_id == current_user.id, from_to).count()
            current_trips = Trip.query.filter(
                Trip.destination.ilike(f'%{search}%'), Trip.user_id == current_user.id, from_to).order_by(direction
                                                                                                          (text(order_by))).offset(offset).limit(TRIPS_PER_PAGE)
        return make_response(jsonify({
            'success': True,
            'trips': [trip.format() for trip in current_trips],
            'count': count

        }), 200)
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
    # print('start date', start_date)
    # print('end date', end_date)
    if end_date < start_date:
        return make_response(jsonify({
            'success': False,
            'error': "End date must be after start date!"
        }), 400)
    comment = body.get('comment', None)
    try:
        new_trip = Trip(destination=destination,
                        start_date=start_date,
                        end_date=end_date,
                        comment=comment,
                        user_id=current_user.id
                        )
        # print(new_trip.format())
        new_trip.insert()
        # offset = get_offset(request)
        # all_trips_count = Trip.query.count()
        # current_trips = Trip.query.order_by(
        #     text('id')).offset(offset).limit(TRIPS_PER_PAGE)
        return make_response(jsonify({
            'success': True,
            'new_trip': new_trip.format(),
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
        # print('start date', start_date)
        # print('end date', end_date)
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
            trip.delete()
            # offset = get_offset(request)
            # all_trips_count = Trip.query.count()
            # current_trips = Trip.query.order_by(
            #     text('id')).offset(offset).limit(TRIPS_PER_PAGE)
            return make_response(jsonify({
                'deleted_trip_id': trip_id,
                'success': True
            }), 200)
        except:
            abort(422)
    else:
        abort(403)

# Get current user trips


@ api.route('/mytrips')
def current_user_trips():
    offset = get_offset(request)
    count = Trip.query.filter(Trip.user_id == current_user.id).count()
    current_trips = Trip.query.filter(
        Trip.user_id == current_user.id).offset(offset).limit(TRIPS_PER_PAGE)
    return jsonify({
        'success': True,
        "trips": [trip.format() for trip in current_trips],
        "count": count
    })
