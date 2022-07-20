from ....database import *
import re

def checkLen(item, lenght):
    try:
        if len(item) < lenght:
            return False
        return True

    except:
        return False

def valEmail(email):

    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return True

        return False

    except:
        return False

def isNameUnique(name):

    try:
        isName = Users.query.filter(Users.name == name).first()
        if isName:
            return False

        return True

    except:
        print('error')
        return False

def isEmailUnique(email):

    try:
        isEmail = Users.query.filter(Users.email == email).first()
        if isEmail:
            return False

        return True

    except:
        return False 
