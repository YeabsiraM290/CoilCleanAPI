from flask import Blueprint
import pandas as pd
import json

from calculation import calculate_on_action
from const import lamp_data
from decorators import *
from convert_data import *

optimize_blueprint = Blueprint('optimize', __name__)

@optimize_blueprint.route('/optimize', methods=["POST"])
@token_required
def optimize(current_user):

    data = {'Lamp type': [],
            'Number of rows': [],
            'Number of columns': [],
            'Distance between lamp and coil, mm': [],
            'Number of lamps': [],
            'Total electric lamp power, W': []
            }

    response1 = request.json['response1']
    response2 = request.json['response2']
    response23 = request.json['response23']
    response231 = request.json['response231']
    option = request.json['option']
    response3 = request.json['response3']
    microorganism_option = request.json['microorganism_option']
    opt_type = request.json['opt_type']

    res_str = calculate_on_action(
        response1, response2, response23, response231, response3, opt_type)
    lamp_names = list(lamp_data)

    try:
        for values in res_str:

            if values[1] is None:
                data['Lamp type'].append(lamp_names[values[0] - 1])
                data['Number of rows'].append('None')
                data['Number of columns'].append('None')
                data['Distance between lamp and coil, mm'].append('None')
                data['Number of lamps'].append('None')
                data['Total electric lamp power, W'].append('None')
            else:
                data['Lamp type'].append(lamp_names[values[0] - 1])
                data['Number of rows'].append(values[1][0])
                data['Number of columns'].append(values[1][1])
                data['Distance between lamp and coil, mm'].append(
                    values[1][2])
                data['Number of lamps'].append(values[1][0] * values[1][1])
                data['Total electric lamp power, W'].append(values[2])
        df4 = pd.DataFrame.from_dict(data)
    except Exception as e:
        return e

    results = convert_data(df4.to_dict())
    return json.dumps({'results': results})
