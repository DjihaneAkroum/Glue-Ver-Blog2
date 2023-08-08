import json
import sys

def ucfirst(s):
    return s[0].upper() + s[1:] if s else ''

def modify_keys(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = ucfirst(key)
            new_value = modify_keys(value)
            new_obj[new_key] = new_value
        return new_obj
    elif isinstance(obj, list):
        return [modify_keys(item) for item in obj]
    else:
        return obj

def replace_values(obj):
    if isinstance(obj, str):
        return obj.replace("prod_", "dev_").replace("prod-", "dev-").replace("glue-jobs-prod", "glue-jobs-dev")
    elif isinstance(obj, dict):
        return {key: replace_values(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_values(item) for item in obj]
    else:
        return obj


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Missing argument")
        print("Usage: python script.py <input_json>")
        sys.exit(1)
    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        data = json.load(f)

    upper_case_keys = modify_keys(data)
    prod_to_dev = replace_values(upper_case_keys)
    dev_output_file = input_file.replace("prod", "dev")
    with open(dev_output_file, 'w') as f:
        json.dump(prod_to_dev, f, indent=2)
