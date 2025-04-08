import glob
import json
from pprint import pprint, pformat


def find_files_path() -> list[str]:
    path = "data/**"
    files = glob.glob(path + "/*.json", recursive=True)
    return files

def json2dict(old_dict: dict) -> dict:
    new_dict = {}

    res = []
    for value in old_dict.values():
        if type(value) in (str, int, float, bool, type(None)):
            res.append(True)
        else:
            res.append(False)
    if all(res):
        return old_dict

    for key, value in old_dict.items():

        if isinstance(value, list) or isinstance(value, tuple):
            for i, item in enumerate(value):
                new_dict[f"{key}[{i}]"] = item
        elif isinstance(value, dict):
            for deep_k, deep_v in value.items():
                new_dict[f"{key}.{deep_k}"] = deep_v
        else:
            new_dict[key] = value

    return json2dict(new_dict)

def main():
    paths = find_files_path()
    for path in paths:
        with open(path, "r") as file:
            old_dict = json.loads(file.read())
            print(f"before: \n{pformat(old_dict)}")

            new_dict = json2dict(old_dict)
            print(f"after: \n{pformat(new_dict)}")


if __name__ == "__main__":
    main()
