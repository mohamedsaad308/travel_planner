# from travel_planner.users_api import api
# from travel_planner.users_api.auth import basic_auth
# from flask import jsonify


# @api.route('/token', methods=['POST'])
# @basic_auth.login_required
# def get_token():
#     token = basic_auth.current_user().get_token()
#     return jsonify({
#         'token': token
#     })
