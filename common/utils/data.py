def group_by(data, keys_value, grouping_keys):
    """
        Method to remove pim 1 dimensional data to nested data.
    :param data: (dict) - Data from which 1 dimensional data are supposed.
    :param keys_value: (list) - List of all the keys in the Data
    :param grouping_keys: (list) - Grouping key.
    :return:
    """
    grouped_values = dict()
    for grouping_key in grouping_keys:
        grouped_values[grouping_key] = dict()

    for key in keys_value.sort():
        values = key.split("_")
        actual_key = values[2]
        group_name = values[1]
        idx = values[0]
        if group_name in grouping_keys:
            if idx not in grouped_values[group_name]:
                grouped_values[group_name][idx] = dict()
            grouped_values[group_name][idx].add(actual_key, data[actual_key])
            del data[actual_key]
    for key, grouped_data in grouped_values.items():
        if not len(data[key]):
            data[key] = list()
        for idx, val in grouped_data['key']:
            data[key].append(val)
    return data

