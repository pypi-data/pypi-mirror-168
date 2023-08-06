from typing import Any, Iterable, List, Type
import re
from keyword import iskeyword


def camel_to_snake(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

def nested_getattr(obj: Type, attrs: List[str]) -> Any:
    return nested_getattr(obj := getattr(obj, attrs.pop(0)), attrs) if attrs else obj

def flatten(d: dict, path: List[str] = []) -> dict:
    result = {}
    for k, v in d.items():
        new_path = path + [k]
        
        if isinstance(v, dict):
            result.update(flatten(v, path=new_path))
        
        result[tuple(new_path)] = v
    return result

def iterables_intersect(a: Iterable, b: Iterable) -> bool:
    return bool(set(a).intersection(set(b)))

def format_alias(attr_name):
    return attr_name[1:] if attr_name.startswith("_") and iskeyword(attr_name[1:]) else attr_name