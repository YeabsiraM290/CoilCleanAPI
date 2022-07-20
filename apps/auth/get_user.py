from flask import Blueprint
from flask import make_response

from ..middlewares.decorators import *

get_blueprint = Blueprint('get', __name__)

@get_blueprint.route('/get', methods=["GET"])
@token_required
def getUser(current_user):

    try:
        user_id = current_user.userid
        userInfo = Users.query.filter(
            Users.userid == int(user_id)).first()

        if userInfo:
            return userInfo.serialize(), 200

        return make_response({"message": "user not found"}, 400)

    except:
        return make_response({"message": "can not get user, exception thrown"}, 400)
 
