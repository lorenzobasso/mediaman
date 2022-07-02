import json


def load_json(filename):
    with open(filename) as f:
        return json.load(f)


def dump_json(data, filename, indent=4, sort_keys=False):
    with open(filename, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=sort_keys)
