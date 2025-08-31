import csv
import json
import ast
from pathlib import Path

def parse_value(value: str, dtype: str):
    """Convert CSV string to proper typed Python object."""
    if dtype == "int":
        return int(value)
    elif dtype == "float":
        return float(value)
    elif dtype == "bool":
        return value.lower() in ("true", "1", "yes")
    elif dtype.startswith("array"):
        # array[int], array[str] etc.
        try:
            parsed = ast.literal_eval(value)  # safely parse list string
            if "int" in dtype:
                return [int(x) for x in parsed]
            elif "float" in dtype:
                return [float(x) for x in parsed]
            elif "bool" in dtype:
                return [str(x).lower() in ("true", "1", "yes") for x in parsed]
            else:  # default string
                return [str(x) for x in parsed]
        except Exception:
            return []
    else:
        return str(value)

def csv_to_json(csv_file, json_file):
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    headers = rows[0]
    schema = rows[1]   # second row defines types
    data_rows = rows[2:]

    result = {}
    for row in data_rows:
        entry = {}
        for i, value in enumerate(row):
            key = headers[i]
            dtype = schema[i]
            entry[key] = parse_value(value, dtype)
        result[entry["id"]] = entry  # use id as lookup key

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"Converted {csv_file} -> {json_file}")

if __name__ == "__main__":
    input_files = ["Player.csv", "Quest.csv", "Purchasable.csv"]
    for file in input_files:
        name = Path(file).stem
        csv_to_json(file, f"{name}.json")
