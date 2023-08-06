import json


def dict2json(dictx: dict, indent=4):
    dict_new = {}
    for k, v in dictx.items():
        if isinstance(v, (bool, tuple, dict, float, int)):
            dict_new[k] = v
        else:
            dict_new[k] = str(v)

    return json.dumps(dict_new, ensure_ascii=False, indent=indent)