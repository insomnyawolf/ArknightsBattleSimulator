import json

def read_json(filepath: str) -> dict:

    with open(filepath) as f:
        return json.load(f)


def write_json(data: dict, filepath: str) -> None:

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

