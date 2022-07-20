from flask import Blueprint
from flask import make_response

from decorators import *

delete_blueprint = Blueprint('delete', __name__)

@delete_blueprint.route('/delete', methods=["DELETE"])
@token_required
def deleteUser(current_user):

    try:
        user_id = current_user.userid
        user = Users.query.filter(
            Users.userid == int(user_id)).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            return make_response({"message": "account deleted succesfuly"}, 200)

        return make_response({"message": "user not found"}, 401)

    except:

        return make_response({"message": "user not deleted, exception thrown"}, 401) 
