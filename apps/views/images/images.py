from flask import Blueprint
from flask import request, jsonify, make_response

from .helpers.get_images import get_response_images
from .helpers.generate_images import generate_images
from ...middlewares.decorators import token_required

get_images_blueprint = Blueprint('images', __name__)

@get_images_blueprint.route('/images', methods=["POST"])
@token_required
def get_images(current_user):

    try:
        response1 = request.json['response1']
        response2 = request.json['response2']
        response23 = request.json['response23']
        response231 = request.json['response231']
        option = request.json['option']
        response3 = request.json['response3']
        microorganism_option = request.json['microorganism_option']
        opt_type = request.json['opt_type']
        generate_images(response1, response2, response23, response231,
                        option, response3, microorganism_option, opt_type)
        encoded_images = get_response_images()

        return jsonify({'images': encoded_images})

    except Exception as e:

        return make_response({ "message": "can not return images, Exception thrown"},400) 
