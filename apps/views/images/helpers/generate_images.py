from ...calculation.calculation import calculate_on_action, build_on_action
from ....constants.const import lamp_data

def generate_images(response1, response2, response23, response231, option, response3, microorganism_option, opt_type):
    lamp_names = list(lamp_data)
    data4 = [[], [], [], [], [], []]
    res_str = calculate_on_action(
        response1, response2, response23, response231, response3, opt_type)

    for value in res_str:
        data4[0].append(lamp_names[value[0] - 1])
        data4[1].append(value[1][0])
        data4[2].append(value[1][1])
        data4[3].append(value[1][2])
        data4[4].append(value[1][0] * value[1][1])
        data4[5].append(value[2])

    res_str1 = []
    for index, row in enumerate(data4[0]):
        if data4[0][1] != 'None':
            res_str1.append(
                [lamp_names.index(data4[0][0]) + 1, (int(data4[1][index]), int(data4[2][index]), float(data4[3][index])), float(data4[5][index])])
        else:
            res_str1.append(['None', ('None', 'None', 'None'), 'None'])

    build_on_action(response1, response2, response23, response231, response3, res_str1, lamp_names.index(option),
                    option,
                    microorganism_option, opt_type)
