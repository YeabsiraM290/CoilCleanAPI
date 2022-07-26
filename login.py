from flask import Blueprint
from flask import request, jsonify, make_response
import datetime as dt
import jwt
from db_helpers import get_user
from settings import SECRET_KEY

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=["GET"])
def login():

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response({'message': 'Invalid information submited'}, 401)

    email = auth.username
    password = auth.password
    user = get_user(email)

    try:
        if user:
            #if bcrypt.checkpw(password.encode('utf-8'), user.password.decode()):
            if password == user.password:
                data = {}
                token = jwt.encode({'account_number': user.userid, 'exp': dt.datetime.utcnow(
                ) + dt.timedelta(hours=24)}, SECRET_KEY)
                data["token"] = token

                return make_response(jsonify(data), 200)

            return make_response({'message': "Email or password not correct."}, 400)
        else:

            return make_response({'message': 'Could not verify, user not found'}, 401)
    except Exception as e:

        return make_response({'message': e}, 401)
