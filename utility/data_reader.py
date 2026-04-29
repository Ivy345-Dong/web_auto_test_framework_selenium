import json
import yaml
import os


# Define method to read JSON file data for test case parameterization
def get_json_data(filename):
    """

    :param filename: File path and file name
    :return: Return data list
    """
    data_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        case_data = json.load(f)
        for case in case_data.values():
            list = case.values()
            data_list.append(tuple(list))
    return data_list

def get_env_url():
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'environment.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['web']['url']