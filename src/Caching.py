

# The method creates a new file with specified name on a special folder
def create_file(filename):
    path = '../Data/%s' % filename
    if not os.path.isfile(path):
        price = open(path, 'w+')
    return path 


# The method compares current data and previous data and creates additional new data
def get_new_data(curr_data, prev_data):
    curr_data = edit_price_data(curr_data)

    data = []

    length_prev = len(prev_data)
    length_curr = len(curr_data)

    start = length_prev - length_curr

    for row in range(length_curr):
        if prev_data.values[start + row][0] != curr_data.values[row][0] and prev_data.values[start + row][0] < curr_data.values[row][0]:
            data.append(curr_data.values[row])

    return data
