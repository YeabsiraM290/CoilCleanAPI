from flask import request, make_response
from functools import wraps
import jwt
from ...database import *
from ...settings import SECRET_KEY

def check_token(token):
    black_listed = BlacklistedTokens.query.filter(BlacklistedTokens.token == token).first()
    if black_listed:
        return True

    return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        try:

            if 'Bearer' in request.headers['Authorization'].split(' ')[0]:
                token = request.headers['Authorization'].split(' ')[1]
            else:
                return "Token is required!", 401
        except:
            return "Token is required!", 401

        try:
            if (not check_token(token=token) ):
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if(data):
                    current_user = Users.query.filter(
                    Users.userid == data['account_number']).first()

                    if current_user == None:
                        return "Account not found!", 400
                else:
                    return "Cannot generate token"

                return f(current_user, *args, **kwargs)

            return "Invalid token", 401

        except Exception as e:
            return make_response({'message': e}, 400)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        else:
            return make_response({"message": "Token is invalid!"}, 401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if(data):
                current_user = Users.query.filter(Users.userid == data['account_number'], Users.role== 0).first()

                if current_user == None:
                    return "Admin required!", 400
     
        except:
            
            return make_response({"message": "Token is invalid!"}, 401)


        return f(current_user, *args, **kwargs)

    return decorated 
    