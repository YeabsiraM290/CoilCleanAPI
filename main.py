from flask import Blueprint

from decorators import *

hello_world_blueprint = Blueprint('hello_world', __name__)

@hello_world_blueprint.route('/')
@token_required
def hello_world():
    return 'This is my first API call!' 
