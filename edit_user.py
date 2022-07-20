from flask import Blueprint
from flask import request, make_response

from validation import checkLen, valEmail, isNameUnique, isEmailUnique
from decorators import *

edit_blueprint = Blueprint('edit', __name__)

@edit_blueprint.route('/edit', methods=["PUT"])
@token_required
def editUser(current_user):
    try:
        user_id = current_user.userid
        user = Users.query.filter(
            Users.userid == int(user_id)).first()

        if user:

            updated_user_info = request.get_json()
            name=''
            email=''
            role=''
            password_from_request=''
            try:
                name = updated_user_info['name']
            except:
                pass
            try:
                email = updated_user_info['email']
            except:
                pass
            try:
                password_from_request = updated_user_info['password']
            except:
                pass
            try:
                role = updated_user_info['role']
            except:
                pass

            if(name):
                if(not isNameUnique(name)):
                    print("nameeee")
                    return make_response({"message": "The name specified is taken"}, 401)
                else:
                    user.name = name

            if(email):
                if(valEmail(email)):
                    if(not isEmailUnique(email)):
                        print("emaillll")
                        return make_response({"message": "The email specified is taken"}, 401)
                    else:
                        user.email = email
                else:
                    print("Inemaillll")
                    return make_response({"message": "Invalid email"}, 401)

            if(password_from_request):
                if(not checkLen(password_from_request, 8)):
                    print("passss")
                    return make_response({"message": "Password must contain more than 8 charcters"}, 401)
                else:
                    user.password = password_from_request

            if(int(role) not in [0,1]):
                print("role")
                return make_response({"message": "invalid role"}, 401)
            else:
                user.role = role

            db.session.add(user)
            db.session.commit()

            return make_response({"message": "user information updated successfully"}, 200)
    except Exception as e:
        return make_response({"message": e}, 401)
