from flask import request, jsonify, make_response,Blueprint
import datetime as dt
import jwt
from validation import checkLen, valEmail, isNameUnique, isEmailUnique
from model import *

signup_blueprint = Blueprint('signup', __name__)
SECRET_KEY = "dfhgfhdjghfdghufdhguifhuitrheui78476375646876uergfjhdsgfh"
@signup_blueprint.route('/signup', methods=["POST"])
def signup():
    try:

        name = request.json['name']
        email = request.json['email']
        password_from_request = request.json['password']
        role = request.json['role']

        if(not isNameUnique(name)):
            return make_response({"message": "The name specified is taken"}, 401)

        if(valEmail(email)):
            if(not isEmailUnique(email)):
                return make_response({"message": "The email specified is taken"}, 402)
        else:
            return make_response({"message": "Invalid email"}, 401)

        if(not checkLen(password_from_request, 8)):
            return make_response({"message": "Password must contain more than 8 charcters"}, 403)

        if(int(role) not in [0,1]):
            return make_response({"message": "invalid role"}, 404)

        # password = bcrypt.hashpw(password_from_request.encode('utf-8'), bcrypt.gensalt())
        new_user = Users(name=name, email=email, password=password_from_request, role=role)

        db.session.add(new_user)
        db.session.commit()

        data = {}
        token = jwt.encode({'account_number': new_user.userid, 'exp': dt.datetime.utcnow(
        ) + dt.timedelta(hours=240)}, SECRET_KEY)
        data["token"] = token

        return make_response(jsonify(data), 200)

    except Exception as e:
        return make_response({"message": e}, 401)

