from flask import Blueprint
from flask import request, make_response
from model import *

logout_blueprint = Blueprint('logout', __name__)

def check_token(token):
    black_listed = BlacklistedTokens.query.filter(BlacklistedTokens.token == token).first()
    if black_listed:
        return True

    return False

@logout_blueprint.route('/logout', methods=["GET"])
def logout():
    token=None

    if 'Bearer' in request.headers['Authorization'].split(' ')[0]:
        token = request.headers['Authorization'].split(' ')[1]
    else:
        return "Token is required!", 401

    try:
        if(not check_token(token)):
            blacklist_token = BlacklistedTokens(token=token)
            db.session.add(blacklist_token)
            db.session.commit()

            return make_response({"message":"Logout succesful"}, 200)

        return make_response({"message":"Logout succesful"}, 200)

    except Exception as e:

        return make_response({'message': e}, 400)
