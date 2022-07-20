from model import *

def get_user(email):
    user = Users.query.filter(Users.email == email).first()

    return user
