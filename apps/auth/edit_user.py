from flask import Blueprint
from flask import request, make_response
import bcrypt

from .constants.roles import *
from .helpers.validation import checkLen, valEmail, isNameUnique, isEmailUnique
from ..middlewares.decorators import *

edit_blueprint = Blueprint('edit', __name__)
roles = Roles.role

@edit_blueprint.route('/edit', methods=["PUT"])
@token_required
def editUser(current_user):
    try:
        user_id = current_user.userid
        user = Users.query.filter(
            Users.userid == int(user_id)).first()

        if user:

            updated_user_info = request.get_json()

            name = updated_user_info['name']
            email = updated_user_info['email']
            password_from_request = updated_user_info['password']
            role_from_request = updated_user_info['role']

            if(name):
                if(not isNameUnique(name)):
                    return make_response({"message": "The name specified is taken"}, 400)
                else:
                    user.name = name

            if(email):
                if(valEmail(email)):
                    if(not isEmailUnique(email)):
                        return make_response({"message": "The email specified is taken"}, 400)
                    else:
                        user.email = email
                else:
                    return make_response({"message": "Invalid email"}, 401)

            if(password_from_request):
                if(not checkLen(password_from_request, 8)):
                    return make_response({"message": "Password must contain more than 8 charcters"}, 400)
                else:
                    password = bcrypt.hashpw(
                        bytes(password_from_request, "UTF-8"), bcrypt.gensalt())
                    user.password = password

            if(int(role_from_request) not in roles.value):
                return make_response({"message": "invalid role"}, 403)
            else:
                user.role = role_from_request

            db.session.add(user)
            db.session.commit()

            return make_response({"message": "user information updated successfully"}, 200)
    except Exception as e:
        return make_response({"message": "user not registered, exception thrown"}, 400)
 
