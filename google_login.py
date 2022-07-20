import jwt
from flask import Blueprint
from flask import request, make_response, session
from google.oauth2 import id_token
import datetime as dt
import google.auth.transport.requests

from db_helpers import get_user
from model import Users, db
SECERET_KEY='dfhgfhdjghfdghufdhguifhuitrheui78476375646876uergfjhdsgfh'
google_login_blueprint = Blueprint('google_login', __name__)

@google_login_blueprint.route('/google_login', methods=["GET"])
def google_login():

        if 'Bearer' in request.headers['Authorization'].split(' ')[0]:
            token = request.headers['Authorization'].split(' ')[1]

            uInfo = id_token.verify_oauth2_token(
                token, google.auth.transport.requests.Request(session))            
            user = get_user(uInfo['email'])

            if user:
                current_user = Users.query.filter(
                Users.email == uInfo['email']).first()
                token = jwt.encode({'account_number': current_user.userid, 'exp': dt.datetime.utcnow(
                ) + dt.timedelta(hours=240)}, SECERET_KEY)
                return make_response({"token":token}, 200)
            else:

                try:
                    new_user = Users(name=uInfo['name'], email=uInfo['email'])
                    db.session.add(new_user)
                    db.session.commit()
                    token = jwt.encode({'account_number': new_user.userid, 'exp': dt.datetime.utcnow(
                    ) + dt.timedelta(hours=240)}, SECERET_KEY)
                    return make_response({"token":token}, 200)
                except Exception as e:
                    
                    return make_response({'message': e}, 400)

        return make_response({'message': e}, 400)
