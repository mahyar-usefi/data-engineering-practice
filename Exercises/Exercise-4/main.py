import glob
import json
import csv


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

def dict2csv(path: str, flattened: dict):
    path = path.replace(".json", ".csv")
    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=flattened.keys())
        writer.writeheader()
        writer.writerow(flattened)

def main():
    paths = find_files_path()
    for path in paths:
        with open(path, "r") as file:
            unflattened = json.loads(file.read())
            flattened = json2dict(unflattened)
            dict2csv(path, flattened)


if __name__ == "__main__":
    main()
