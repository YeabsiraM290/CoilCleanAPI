def convert_data(data):
    keys = ["Lamp type", "Number of rows", "Number of columns",
        "Distance between lamp and coil, mm", "Number of lamps", "Total electric lamp power, W"]
    table_data = {
        "Lamp type": [],
        "Number of rows": [],
        "Number of columns": [],
        "Distance between lamp and coil, mm": [],
        "Number of lamps": [],
        "Total electric lamp power, W": [],
    }
    length = len(data[keys[0]])
    for row in range(0, 6):
        row_data = []
        for value in range(0, length):
            row_data.append(data[keys[row]][value])

        table_data[keys[row]] = row_data;

    rows = [];
    for count in range(0, length):
        row_data = []
        row_data.append(table_data[keys[0]][count])
        row_data.append(data[keys[1]][count])
        row_data.append(data[keys[2]][count])
        row_data.append(data[keys[3]][count])
        row_data.append(data[keys[4]][count])
        row_data.append(data[keys[5]][count])

        rows.append(row_data)

    return rows;
