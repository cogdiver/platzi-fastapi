import json


def get_filename_json(path):
    """
    get the data from a file in a json format
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def write_filename_json(path, content):
    """
    write a file in a json format
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False))


def validate_unique_key(value, values_dict, key, err):
    """
    valide if a value in a key is unique
    """
    keys = list(map(lambda c: c[key], values_dict))
    if value in keys:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: {err}'"
        )


def validate_valid_key(value, values_dict, key, err):
    """
    valide if a value in a key is valid
    """
    keys = list(map(lambda c: c[key], values_dict))
    if value in keys:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: {err}"
        )
