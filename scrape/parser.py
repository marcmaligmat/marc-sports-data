from typing import Callable, Optional


def save_entry(
    custom_dict: dict,
    resp_dict: dict,
    func: Optional[Callable[[dict, dict], str]],
    prefix: Optional[str] = "",
) -> dict:
    """Return referencing custom dict to response dict"""
    r = {}
    for key in custom_dict:
        value = func(custom_dict[key], resp_dict)
        key = prefix + key
        r.update({key: value})
    return r


def assign_var(key: str, dic: dict) -> str:
    return dic[key] if is_key_exists(key, dic) else "_"


def is_key_exists(key: str, dic: dict) -> bool:
    return key in dic
