import json


def read_file(filename):
    data = {}
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except (IOError, FileNotFoundError) as e:
        print("Unable to read file: ", filename, " | error: ", e)
    return data
