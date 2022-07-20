from flask import Blueprint
from flask import request, make_response
from ...database import *

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route('/logout', methods=["GET"])
def logout():
    token=None

    if 'Bearer' in request.headers['Authorization'].split(' ')[0]:
        token = request.headers['Authorization'].split(' ')[1]
    else:
        return "Token is required!", 401

    try:
        blacklist_token = BlacklistedTokens(token=token)
        db.session.add(blacklist_token)
        db.session.commit()

        return make_response({"message":"Logout succesful"}, 200)


    except Exception as e:

        return make_response({'message': "can not logout exeception thrown"}, 400)
