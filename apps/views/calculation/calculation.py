import csv
import tempfile

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches

image_path = 'generated_files/images/'

# don't touch 
def calculate_input_geometry(nx, ny, diameter_l, length_l, length_arc_l, num_lamps_y, num_lamps_x):
    num_lamps = num_lamps_y * num_lamps_x
    delta_x = (nx / num_lamps_x - length_l) / 2
    delta_y = ny / num_lamps_y / 2
    x_l_1 = delta_x + (2 * delta_x + length_l) * np.arange(num_lamps_x)
    y_l_1 = delta_y * (1 + 2 * np.arange(num_lamps_y))
    v_x_l = np.tile(x_l_1, num_lamps_y)
    y_l = np.tile(y_l_1, (num_lamps_x, 1))
    v_y_l = (np.transpose(y_l)).reshape(-1)
    v_diameter_l = np.repeat(diameter_l, num_lamps)
    v_length_l = np.repeat(length_l, num_lamps)
    v_length_arc_l = np.repeat(length_arc_l, num_lamps)
    v_orientation_l = [1] * num_lamps
    return v_diameter_l, v_length_l, v_length_arc_l, v_x_l, v_y_l, v_orientation_l

def draw_lamps_location(l_radius, l_length, x0, y0, l_orientation, nx, ny, h, file_name):
    num_lamps = len(l_orientation)
    nxy = (nx + ny) / 2
    k = 8.0 / nxy
    kx = max(6, round(k * nx))
    ky = max(6, round(k * ny))
    fig = plt.figure(figsize=(kx, ky))
    # fig = plt.figure(figsize=(8, 6))  # facecolor="#f1f1f1")
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes((left, bottom, width, height))  # , facecolor="#e1e1e1")
    ax.set_xlim((0, nx + 1))
    ax.set_ylim((0, ny + 1))
    ax.grid(visible=True, which='major', axis='both')
    ax.plot(np.linspace(0, nx, nx + 1), np.zeros((nx + 1, 1)), color="black", linewidth=3)
    ax.plot(np.linspace(0, nx, nx + 1), np.ones((nx + 1, 1)) * (ny + 1), color="black", linewidth=3)
    ax.plot(np.zeros((ny + 1, 1)), np.linspace(0, ny, ny + 1), color="black", linewidth=3)
    ax.plot(np.ones((ny + 1, 1)) * (nx + 1), np.linspace(0, ny, ny + 1), color="black", linewidth=3)
    rect = mpatches.Rectangle((0, 0), nx + 1, ny + 1,
                              # fill=False,
                              # alpha=0.1,
                              color="navajowhite",
                              # linewidth=5,
                              # facecolor="darkgoldenrod"
                              )
    plt.gca().add_patch(rect)

    for n in range(num_lamps):
        if l_orientation[n] == 1:
            rect = mpatches.Rectangle((x0[n], y0[n] - l_radius[n]), l_length[n], l_radius[n] * 2,
                                      # fill=False,
                                      # alpha=0.1,
                                      color="sandybrown",
                                      # linewidth=2,
                                      # facecolor="chocolate"
                                      )
            text_x = x0[n] + l_length[n] / 2 - 4
            text_y = y0[n] + l_radius[n] + 2
            # text_x1 = x0[n] - 4
            # text_y1 = y0[n] + l_radius[n] + 2
        else:
            rect = mpatches.Rectangle((x0[n] - l_radius[n], y0[n]), l_radius[n] * 2, l_length[n],
                                      # fill=False,
                                      # alpha=0.1,
                                      color="sandybrown",
                                      # linewidth=2,
                                      # facecolor="chocolate"
                                      )
            text_x = x0[n] + l_radius[n] + 2
            text_y = y0[n] + l_length[n] / 2 - 2
            # text_x1 = x0[n] + l_radius[n] + 2
            # text_y1 = y0[n] - 4
        plt.gca().add_patch(rect)
        plt.plot(x0[n], y0[n], marker=".", markersize=4, color='blue')
        ax.text(text_x, text_y, 'L' + str(int(n + 1)))  # , fontsize=l_radius[n]
        # ax.text(text_x1, text_y1, 'x=' + str(int(x0[n])) + ',y=' +str(int(y0[n])))  # , fontsize=l_radius[n]
    plt.title(r'Lamps Arrangement Over the Coil at a Distance ' + str(int(h)) + 'mm')
    ax.set_xlabel('Coil width, mm')
    ax.set_ylabel('Coil height, mm')
    plt.savefig(file_name)
    return 0

def calculate_vf_special_matrix(l_radius, l_length, l_height, shift_x, y0, nx, ny):
    # x0 = 0, nx<=l
    # matrix_vf = np.zeros((ny, nx))
    e = l_length / l_radius
    h = l_height / l_radius
    matrix_x = np.tile(range(nx), (ny, 1))
    matrix_x = (matrix_x + shift_x) / l_radius
    matrix_y = np.tile(range(ny), (nx, 1))
    matrix_y = (np.transpose(matrix_y) - y0) / l_radius

    b = matrix_y * matrix_y + h * h
    a = matrix_x * matrix_x + b
    c = (e - matrix_x) * (e - matrix_x)
    am = a - 1
    bm = b - 1
    bs = np.sqrt(b)
    ac1 = np.arccos((matrix_x * matrix_x - bm) / am)
    ac2 = np.arccos((c - bm) / (c + bm))
    ac3 = np.arccos((matrix_x * matrix_x - bm) / am / bs)
    ac4 = np.arccos((c - bm) / (c + bm) / bs)
    ac5 = np.arccos(1 / bs)

    matrix_vf = h / b - h / (2 * np.pi * b) * (ac1 + ac2
                                               - matrix_x * (a + 1) / np.sqrt(am * am + 4 * matrix_x * matrix_x) * ac3
                                               - np.sqrt(c) * (c + b + 1) / np.sqrt((c + bm) * (c + bm) + 4 * c) * ac4
                                               + e * ac5)
    return matrix_vf

def build_coil_intensities_matrix_l(l_radius, l_length, l_height, x0, y0, nx, ny, l_intensity):
    # x0 = Any int, nx = Any int
    x0 = int(round(x0))
    l_length = int(round(l_length))
    matrix_vf_1 = calculate_vf_special_matrix(l_radius, l_length + x0, l_height, 0, y0, x0, ny) \
                  - calculate_vf_special_matrix(l_radius, x0, l_height, 0, y0, x0, ny)

    matrix_vf_2 = calculate_vf_special_matrix(l_radius, l_length, l_height, 0, y0, l_length, ny)

    matrix_vf_3 = calculate_vf_special_matrix(l_radius, nx - x0, l_height, l_length, y0, nx - x0 - l_length, ny) \
                  - calculate_vf_special_matrix(l_radius, nx - x0 - l_length, l_height, 0, y0, nx - x0 - l_length, ny)

    matrix_vf = np.concatenate((matrix_vf_1, matrix_vf_2, matrix_vf_3), axis=1)
    matrix_intensity = l_intensity * matrix_vf
    return matrix_intensity

def build_coil_intensities_matrix(diameter_l, length_l, length_arc_l, h, x_l, y_l, nx, ny, intensity_l,
                                  orientation_l):
    matrix_intensity = np.zeros((ny, nx))
    num_lamps = len(length_l)

    for nl in range(num_lamps):
        if orientation_l[nl] == 1:
            x0 = x_l[nl] + (length_l[nl] - length_arc_l[nl]) / 2
            y0 = y_l[nl]
            matrix_intensity = matrix_intensity + build_coil_intensities_matrix_l(diameter_l[nl] / 2, length_arc_l[nl],
                                                                                  h, x0, y0, nx, ny, intensity_l[nl])
        else:
            x0 = x_l[nl]
            y0 = y_l[nl] + (length_l[nl] - length_arc_l[nl]) / 2
            matrix_intensity = matrix_intensity + build_coil_intensities_matrix_l(diameter_l[nl] / 2, length_arc_l[nl],
                                                                                  h, y0, x0, ny, nx, intensity_l[nl]).T
    return matrix_intensity

def create_time_figures(nx, ny, matrix_time):
    nxy = (nx + ny) / 2
    k = 8 / nxy
    kx = max(6, round(k * nx))
    ky = max(6, round(k * ny))
    fig = plt.figure(figsize=(kx, ky))
    x = np.linspace(0, nx, nx)
    y = np.linspace(0, ny, ny)
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes((left, bottom, width, height))
    # plt.contourf(x, y, matrix_time, 20, cmap='viridis', alpha=0.3)
    cs = plt.contour(x, y, matrix_time, 20, cmap='viridis')
    plt.clabel(cs, inline=1, fmt='%d', fontsize=8)
    plt.title('Microorganism Inactivation Time in minutes')
    ax.set_xlabel('Coil width, mm')
    ax.set_ylabel('Coil height, mm')
    plt.savefig(image_path+'Inactivation Time')
    del fig

    vv = np.flip(np.sort(matrix_time, axis=None))
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_axes((left, bottom, width, height))
    plt.hist(vv, 50, density=True, cumulative=-1, facecolor='g')
    plt.title('Reversed Cumulative Histogram of Microorganism Inactivation Time in min')
    ax.set_xlabel(r'Inactivation time, min')
    ax.set_ylabel('Cumulative probability')
    vv_min = np.min(vv)
    vv_avg = np.mean(vv)
    vv_max = np.max(vv)
    plt.text(0.7 * vv_max + 0.3 * vv_min, 0.9, 'max time = ' + str(int(vv_max)) + 'min')
    plt.text(0.7 * vv_max + 0.3 * vv_min, 0.83, 'avg time = ' + str(int(vv_avg)) + 'min')
    plt.text(0.7 * vv_max + 0.3 * vv_min, 0.76, 'min time = ' + str(int(vv_min)) + 'min')

    plt.grid()
    plt.savefig(image_path+'Inactivation Time Distribution')
    del fig

    # fig = plt.figure(figsize=(8, 8))
    # left, bottom, width, height = 0.1, 0.1, 0.9, 0.9
    # ax = fig.add_axes((left, bottom, width, height))
    # xx, yy = np.meshgrid(x, y)
    # ax = plt.axes(projection='3d')
    # ax.plot_surface(xx, yy, matrix_intensity, cmap='viridis')
    # ax.view_init(60, 30)
    # ax.set_xlabel('Coil width, mm')
    # ax.set_ylabel('Coil height, mm')
    # ax.set_zlabel(r'Intensity, $\mu$W/$cm^2$')
    # plt.savefig(r'Coil Intensities 3D')

    return 0

def create_intensity_figures(nx, ny, matrix_intensity):
    nxy = (nx + ny) / 2
    k = 8 / nxy
    kx = max(6, round(k * nx))
    ky = max(6, round(k * ny))
    fig = plt.figure(figsize=(kx, ky))
    x = np.linspace(0, nx, nx)
    y = np.linspace(0, ny, ny)
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes((left, bottom, width, height))
    # plt.contourf(x, y, matrix_intensity, 20, cmap='viridis', alpha=0.3)
    cs = plt.contour(x, y, matrix_intensity, 20, cmap='viridis')
    plt.clabel(cs, inline=1, fmt='%d', fontsize=8)
    plt.title(r'Irradiation Intensity, $\mu$W/$cm^2$')
    ax.set_xlabel('Coil width, mm')
    ax.set_ylabel('Coil height, mm')
    plt.savefig(image_path+'Coil Intensities')
    del fig

    vv = np.sort(matrix_intensity, axis=None)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_axes((left, bottom, width, height))
    plt.hist(vv, 50, density=True, cumulative=True, facecolor='g')
    plt.title('Cumulative Histogram of Irradiation Intensity')
    ax.set_xlabel(r'Irradiation intensity, $\mu$W/$cm^2$')
    ax.set_ylabel('Cumulative probability')
    vv_min = np.min(vv)
    vv_avg = np.mean(vv)
    vv_max = np.max(vv)
    plt.text(vv_min, 0.9, 'min intensity = ' + str(int(vv_min)) + '$\mu$W/$cm^2$')
    plt.text(vv_min, 0.83, 'avg intensity = ' + str(int(vv_avg)) + '$\mu$W/$cm^2$')
    plt.text(vv_min, 0.76, 'max intensity = ' + str(int(vv_max)) + '$\mu$W/$cm^2$')
    plt.grid()
    plt.savefig(image_path+'Coil Intensities Distribution')
    del fig

    fig = plt.figure(figsize=(8, 8))
    # left, bottom, width, height = 0.1, 0.1, 0.9, 0.9
    ax = fig.add_axes((left, bottom, width, height))
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.title('Irradiation Intensity 3D')
    xx, yy = np.meshgrid(x, y)
    ax = plt.axes(projection='3d')
    ax.plot_surface(xx, yy, matrix_intensity, cmap='viridis')
    ax.view_init(60, 30)
    ax.set_xlabel('Coil width, mm')
    ax.set_ylabel('Coil height, mm')
    ax.set_zlabel(r'Intensity, $\mu$W/$cm^2$')
    plt.savefig(r''+image_path+'Coil Intensities 3D')

    return 0

def calculate_vf_special_matrix_points(l_radius, l_length, l_height, shift_x, y0, vector_x, vector_y):
    # x0 = 0, nx<=l
    # matrix_vf = np.zeros((num_y, num_x))
    num_x = len(vector_x)
    num_y = len(vector_y)
    e = l_length / l_radius
    h = l_height / l_radius
    matrix_x = np.tile(vector_x, (num_y, 1))
    matrix_x = (matrix_x + shift_x) / l_radius
    matrix_y = np.tile(vector_y, (num_x, 1))
    matrix_y = (np.transpose(matrix_y) - y0) / l_radius

    b = matrix_y * matrix_y + h * h
    a = matrix_x * matrix_x + b
    c = (e - matrix_x) * (e - matrix_x)
    am = a - 1
    bm = b - 1
    bs = np.sqrt(b)
    ac1 = np.arccos((matrix_x * matrix_x - bm) / am)
    ac2 = np.arccos((c - bm) / (c + bm))
    ac3 = np.arccos((matrix_x * matrix_x - bm) / am / bs)
    ac4 = np.arccos((c - bm) / (c + bm) / bs)
    ac5 = np.arccos(1 / bs)

    matrix_vf = h / b - h / (2 * np.pi * b) * (ac1 + ac2
                                               - matrix_x * (a + 1) / np.sqrt(am * am + 4 * matrix_x * matrix_x) * ac3
                                               - np.sqrt(c) * (c + b + 1) / np.sqrt((c + bm) * (c + bm) + 4 * c) * ac4
                                               + e * ac5)
    return matrix_vf

def calculate_coil_vf_point(diameter_l, length_l, length_arc_l, h, x_l, y_l, x, y, orientation_l):
    num_lamps = len(length_l)
    value_vf = 0
    for nl in range(num_lamps):
        if orientation_l[nl] == 1:
            x0 = x_l[nl] + (length_l[nl] - length_arc_l[nl]) / 2
            y0 = y_l[nl]
            value_vf = value_vf + calculate_vf_special_matrix_points(diameter_l[nl] / 2, length_arc_l[nl] + x0, h, 0,
                                                                     y0, x, y) \
                       - calculate_vf_special_matrix_points(diameter_l[nl] / 2, x0, h, 0, y0, x, y)

        else:
            x0 = x_l[nl]
            y0 = y_l[nl] + (length_l[nl] - length_arc_l[nl]) / 2
            value_vf = value_vf + calculate_vf_special_matrix_points(diameter_l[nl] / 2, length_arc_l[nl] + y0, h, 0,
                                                                     x0, y, x) \
                       - calculate_vf_special_matrix_points(diameter_l[nl] / 2, y0, h, 0, x0, y, x)
    return value_vf

def build_optimization_by_h(nx, ny, diameter_l, length_l, length_arc_l, num_rows, num_columns, h_vector):
    # for the specific lamp
    x = np.array([0])
    y = np.array([0])
    v_diameter_l, v_length_l, v_length_arc_l, v_x_l, v_y_l, v_orientation_l = \
        calculate_input_geometry(nx, ny, diameter_l, length_l, length_arc_l, num_rows, num_columns)
    values_h = calculate_coil_vf_point(v_diameter_l, v_length_l, v_length_arc_l, h_vector,
                                       v_x_l, v_y_l, x, y, v_orientation_l)
    max_vf = np.amax(values_h)
    h_max_vf = h_vector[np.argmax(values_h)]
    return max_vf, h_max_vf

def find_optimal_configuration_for_lamp_type(nx, ny, diameter_l, length_l, length_arc_l,
                                             num_rows, num_columns, h_vector, vf_min_req):
    exist_configuration = 0
    num_rows_opt = num_rows
    num_columns_opt = num_columns
    num_lamps_opt = num_rows_opt * num_columns_opt
    cost_opt = num_lamps_opt
    for m in range(1, num_rows + 1):
        for n in range(1, num_columns + 1):
            if exist_configuration and m * n > num_lamps_opt:
                continue
            max_vf, h_max_vf = build_optimization_by_h(nx, ny, diameter_l, length_l, length_arc_l,
                                                       m, n, h_vector)
            if max_vf >= vf_min_req and m * n - max_vf < cost_opt:
                exist_configuration = 1
                num_rows_opt = m
                num_columns_opt = n
                num_lamps_opt = num_rows_opt * num_columns_opt
                cost_opt = num_lamps_opt - max_vf
                h_opt = h_max_vf
                # vf_opt = max_vf
    if exist_configuration == 0:
        return None
    return [num_rows_opt, num_columns_opt, h_opt]

def optimize_installation_exact(nx, ny, min_intensity_req_SI, table_name, downstream_coeff, refl_l, delta_x, delta_y,     h_max):
    data = pd.read_csv(table_name)
    lengths_l = np.array(data.iloc[:, 3])
    lengths_arc_l = np.array(data.iloc[:, 4])
    d_l = np.array(data.iloc[:, 5])
    power_l = np.array(data.iloc[:, 6])
    uvc_eff_l = np.array(data.iloc[:, 8])
    aging_l = np.array(data.iloc[:, 9])
    intensity_eff_l = power_l * uvc_eff_l * aging_l * (1 + refl_l) * downstream_coeff \
                      / (np.pi * d_l * lengths_arc_l)  # W/sq.mm
    vf_min_req = min_intensity_req_SI / (intensity_eff_l * 10 ** 6)
    num_lamps = len(lengths_l)

    h_min = 95

    if h_max - h_min > 205:
        step = 5
    else:
        step = 1
    num_h = int((h_max - h_min) / step + 1)
    h_vector = np.linspace(h_max, h_min, num_h)

    lamps_distribution = []
    ll = lengths_l + 2 * delta_x
    n_lamps_max = (np.floor(nx / ll)).astype(int)
    m_lamps_max = (np.floor(ny / (delta_y * 2))).astype(int)
    for nl in range(num_lamps):
        if n_lamps_max[nl] == 0 or m_lamps_max == 0:
            lamps_distribution.append([nl + 1, None, 'Lamp_size'])
            continue
        vector_opt = find_optimal_configuration_for_lamp_type(nx, ny, d_l[nl], lengths_l[nl], lengths_arc_l[nl],
                                                              m_lamps_max, n_lamps_max[nl], h_vector, vf_min_req[nl])
        if vector_opt is None:
            lamps_distribution.append([nl + 1, None, 'Intensity'])
        else:
            total_power = power_l[nl] * vector_opt[0] * vector_opt[1]
            opt = [nl + 1, vector_opt, round(total_power, 1)]
            lamps_distribution.append(opt)

    return lamps_distribution

def calculate_survival_time(intensity, k, confidence):
    # intensity - W/sq.m ; k - sq.m/J ; confidence < 1
    # s_time - sec
    s_time = -np.log(1 - confidence) / intensity / k
    return s_time

def calculate_on_action(response1, response2,response23,response231, response3, opt_type):
    try:
        lamps_data_file = 'Lamps_data.csv'
        temp = tempfile.NamedTemporaryFile(prefix='Duct Information', suffix='.csv')
        with open(temp.name, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["Duct Information","Value"])
            headers = ['x', 'y', 'downstream_coeff', "max_dist_to_coil"]
            for header in headers:
                writer.writerow([header,response1[header]])

        temp = tempfile.NamedTemporaryFile(prefix='Common Information', suffix='.csv')
        with open(temp.name, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["Common Information","Value"])
            headers = ['reflection_coeff', 'min-dist-wall-x', 'min-dist-wall-y']
            for header in headers:
                writer.writerow([header,response3[header]])

        if opt_type == 'Microorganism':
            temp = tempfile.NamedTemporaryFile(prefix='Target information', suffix='.csv')
            with open(temp.name, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow([".","Value"])
                headers = ['required_inactivation_rate', 'max-inactivation_time']
                for header in headers:
                    writer.writerow([header,response2[header]])

            temp = tempfile.NamedTemporaryFile(prefix='Common Information obj', suffix='.csv')
            with open(temp.name, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(["Target Information","Value"])
                headers = ['susceptibilityc_coefficient']
                for header in headers:
                    writer.writerow([header,response23[header]])

            confidence = response2['required_inactivation_rate'] / 100
            min_disact_time = response2['max-inactivation_time'] * 60  # sec
            #####
            susc_k = response23['susceptibilityc_coefficient']
            min_intensity_req_SI = -np.log(1 - confidence) / susc_k / min_disact_time
            ############

        if opt_type == 'Intensity':
            temp = tempfile.NamedTemporaryFile(prefix='Common Information obj intensity', suffix='.csv')
            with open(temp.name, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(["Target Information","Value"])
                headers = ['minimum_UV_irr_intensity']
                for header in headers:
                    writer.writerow([header,response231[header]])

            min_intensity_req_mW_cm2 = response231['minimum_UV_irr_intensity']
            min_intensity_req_SI = min_intensity_req_mW_cm2 / 100

        refl_l = response3['reflection_coeff']
        delta_x = response3['min-dist-wall-x']
        delta_y = response3['min-dist-wall-y']

        ############
        nx = round(response1['x'])
        ny = round(response1['y'])
        downstream_coeff = response1['downstream_coeff']
        h_max= response1['max_dist_to_coil']
        #####

        return optimize_installation_exact(nx, ny, min_intensity_req_SI, lamps_data_file, downstream_coeff,
                                           refl_l, delta_x, delta_y, h_max)

    except Exception as e:
        print(e)
        return 'Fill right values'

def build_on_action(response1, response2,response23,response231, response3, lamps_distribution, lamp_type, lamp_option, microorganism_option, opt_type):
    try:
        lamps_data_file = 'Lamps_data.csv'
        nx = response1["x"]
        ny = response1["y"]
        downstream_coeff = response1["downstream_coeff"]
        #####

        refl_l = response3["reflection_coeff"]

        data = pd.read_csv(lamps_data_file)
        length_l = np.array(data.iloc[lamp_type, 3])
        length_arc_l = np.array(data.iloc[lamp_type, 4])
        d_l = np.array(data.iloc[lamp_type, 5])
        power_l = np.array(data.iloc[lamp_type, 6])
        uvc_eff_l = np.array(data.iloc[lamp_type, 8])
        aging_l = np.array(data.iloc[lamp_type, 9])

        intensity_eff_l = power_l * uvc_eff_l * aging_l * (1 + refl_l) * downstream_coeff \
                          / (np.pi * d_l * length_arc_l)  # W/sq.mm
        num_lamps_y, num_lamps_x, h_opt = lamps_distribution[lamp_type][1]

        diameter_l, length_l, length_arc_l, x_l, y_l, orientation_l = \
            calculate_input_geometry(nx, ny, d_l, length_l, length_arc_l, num_lamps_y, num_lamps_x)
        num_lamps = num_lamps_y * num_lamps_x
        intensity_eff_l = np.repeat(intensity_eff_l, num_lamps)
        orientation_l = [1] * num_lamps
        draw_lamps_location(diameter_l / 2, length_l, x_l, y_l, orientation_l, nx, ny, h_opt,
                            image_path+"Optimal Lamps Arrangement.png")
        matrix_intensity = build_coil_intensities_matrix(diameter_l, length_l, length_arc_l, h_opt, x_l, y_l, nx, ny,
                                                         intensity_eff_l, orientation_l)
        matrix_intensity = matrix_intensity * 10 ** 6  # convert W/sq.mm into W/sq.m

        ############
        if opt_type == 'Microorganism':
            confidence = float(response2['required_inactivation_rate'] / 100)
            
            susc_k = response23['susceptibilityc_coefficient']
            matrix_time = calculate_survival_time(matrix_intensity, susc_k, confidence)
            matrix_time = matrix_time / 60  # sec to minutes
            min_time = int(np.min(matrix_time))
            max_time = int(np.max(matrix_time))
            avg_time = int(np.mean(matrix_time))
            create_time_figures(nx, ny, matrix_time)
        if opt_type == 'Intensity':
            min_time, max_time, avg_time = -1, -1 , -1
        matrix_intensity = matrix_intensity * 100  # convert W/sq.m into micro_W/sq.cm
        min_intensity = int(np.min(matrix_intensity))
        max_intensity = int(np.max(matrix_intensity))
        avg_intensity = int(np.mean(matrix_intensity))
        create_intensity_figures(nx, ny, matrix_intensity)
        total_input_power = power_l * num_lamps

        x_l = [int(el) for el in x_l]
        y_l = [int(el) for el in y_l]
        temp = tempfile.NamedTemporaryFile(prefix='report_history', suffix='.csv')
        with open(temp.name, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            np.savetxt(tempfile.NamedTemporaryFile(prefix='x_l', suffix='.csv'), x_l, delimiter=",")
            np.savetxt(tempfile.NamedTemporaryFile(prefix='y_l', suffix='.csv'), y_l, delimiter=",")
            writer.writerow(
                [nx, ny, h_opt, downstream_coeff, num_lamps, total_input_power, min_intensity, avg_intensity,
                 max_intensity, matrix_intensity, min_time, max_time, avg_time, microorganism_option, lamp_option, num_lamps_y, num_lamps_x, opt_type])
        return 'Right'
    except Exception as e:
        print(e)
        return 'Fill right values'
