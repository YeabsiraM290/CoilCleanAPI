from flask import Blueprint
from flask import request, jsonify

from .calculation.calculation import calculate_on_action, build_on_action
from ..constants.const import lamp_data
from ..middlewares.decorators import *

test_post_blueprint = Blueprint('testpost', __name__)

@test_post_blueprint.route('/post', methods=["POST"])
@token_required
def testpost():
    response1 = request.json['response1']
    response2 = request.json['response2']
    response23 = request.json['response23']
    response231 = request.json['response231']
    option = request.json['option']
    response3 = request.json['response3']
    microorganism_option = request.json['microorganism_option']
    opt_type = request.json['opt_type']

    lamp_names = list(lamp_data)

    data4 = [[], [], [], [], [], []]

    res_str = calculate_on_action(
        response1, response2, response23, response231, response3, opt_type)

    for element in res_str:
        data4[0].append(lamp_names[element[0] - 1])
        data4[1].append(element[1][0])
        data4[2].append(element[1][1])
        data4[3].append(element[1][2])
        data4[4].append(element[1][0] * element[1][1])
        data4[5].append(element[2])

    res_str1 = []
    for index, row in enumerate(data4[0]):
        if data4[0][1] != 'None':
            res_str1.append(
                [lamp_names.index(data4[0][0]) + 1, (int(data4[1][index]), int(data4[2][index]), float(data4[3][index])), float(data4[5][index])])
        else:
            res_str1.append(['None', ('None', 'None', 'None'), 'None'])
    print(option)

    build_on_action(response1, response2, response23, response231, response3, res_str1, lamp_names.index(option),
                    option,
                    microorganism_option, opt_type)

    return jsonify(response3) 
