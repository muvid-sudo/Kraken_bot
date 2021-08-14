import os
import pandas as pd


def write_file(path, data, headers):
    if os.stat(path).st_size != 0:
        stored_data = pd.read_csv(path)
        new_data = stored_data.append(data)
        new_data.drop_duplicates(subset=new_data.columns.values[0], keep='last', inplace=True)
        new_data.to_csv(path, encoding='utf-8', index=False, columns=headers, header=True)
    else:
        data.to_csv(path, encoding='utf-8', index=False, columns=headers, header=True)


def creation_or_updation_table_file(filename, data, headers):
    data = pd.DataFrame(data, columns=headers)
    path = create_file(filename)
    new_data = data
    write_file(path, data, headers)


# The method creates a new file with specified name on a special folder
def create_file(filename):
    path = '../Data/%s' % filename
    if not os.path.isfile(path):
        price = open(path, 'w+')
    return path 


# The method compares current data and previous data and creates additional new data
def get_new_data(curr_data, prev_data):


    return new_data
