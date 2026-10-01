import csv
import glob
import json


def find_files_path() -> list[str]:
    path = "data/**"
    files = glob.glob(path + "/*.json", recursive=True)
    return files


def json2dict(old_dict: dict) -> dict:
    final_dict = {}

    if all([isinstance(value, (str, int, float, bool, type(None))) for value in old_dict.values()]):
        return old_dict

    for key, value in old_dict.items():

        if isinstance(value, list) or isinstance(value, tuple):
            for i, item in enumerate(value):
                final_dict[f"{key}[{i}]"] = item
        elif isinstance(value, dict):
            for inner_k, inner_v in value.items():
                final_dict[f"{key}.{inner_k}"] = inner_v
        else:
            final_dict[key] = value

    return json2dict(final_dict)


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
