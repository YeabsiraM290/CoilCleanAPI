from flask import Blueprint
from flask import request, jsonify, make_response
import bcrypt
import datetime as dt
import jwt
from .constants.roles import *
from .helpers.validation import checkLen, valEmail, isNameUnique, isEmailUnique
from ...database import *
from ...settings import SECRET_KEY

signup_blueprint = Blueprint('signup', __name__)
roles = Roles.role

@signup_blueprint.route('/signup', methods=["POST"])
def signup():
    try:

        name = request.json['name']
        email = request.json['email']
        password_from_request = request.json['password']
        role_from_request = request.json['role']

        if(not isNameUnique(name)):
            return make_response({"message": "The name specified is taken"}, 400)

        if(valEmail(email)):
            if(not isEmailUnique(email)):
                return make_response({"message": "The email specified is taken"}, 400)
        else:
            return make_response({"message": "Invalid email"}, 401)

        if(not checkLen(password_from_request, 8)):
            return make_response({"message": "Password must contain more than 8 charcters"}, 400)

        if(int(role_from_request) not in roles.value):
            return make_response({"message": "invalid role"}, 403)

        password = bcrypt.hashpw(
            password_from_request.encode('utf-8'), bcrypt.gensalt())
        new_user = Users(name=name, email=email,
                         password=password, role=role_from_request)

        db.session.add(new_user)
        db.session.commit()

        data = {}
        token = jwt.encode({'account_number': new_user.userid, 'exp': dt.datetime.utcnow(
        ) + dt.timedelta(hours=240)}, SECRET_KEY)
        data["token"] = token

        return make_response(jsonify(data), 200)

    except Exception as e:
        return make_response({"message": e}, 400)
