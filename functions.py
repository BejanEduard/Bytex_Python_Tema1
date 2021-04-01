import json


def dict_from_json(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)

        return data


def print_dict(dictionary, result=""):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print_dict(value, f"{result}{key}.")
        else:
            print(f"{result}{key}.{value}")


my_input = {'a': 1,
            'b': {'c': 2},
            'd': {
                'e': {'f': 3},
                'g': 4
                }
            }

print_dict(my_input)

# actors = dict_from_json('./data/actors.json')
#
# print(f"Type: {type(actors)}")
# for id, info in actors.items():
#     print(f"{id}  :  {info}")

