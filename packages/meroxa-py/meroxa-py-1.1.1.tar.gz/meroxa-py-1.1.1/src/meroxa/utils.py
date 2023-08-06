import json
from json import JSONDecodeError
from typing import Type

from .types import MeroxaApiResponse


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "repr_json"):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)


class ErrorResponse(object):
    def __init__(self, code: str, message: str, details=None) -> None:
        self.code = code
        self.message = message
        self.details = details


def parse_error_message(error):
    try:
        return ErrorResponse(**json.loads(error))
    except JSONDecodeError or TypeError:
        split = error.split("\n", 1)
        return ErrorResponse("Error", split[0])


def api_response(return_type: Type[MeroxaApiResponse]):
    def inner(func):
        async def wrapper(*args, **kwargs):
            res = await func(*args, **kwargs)
            try:
                parsed = json.loads(res)
                if isinstance(parsed, list):
                    return None, [return_type(**par) for par in parsed]
                return None, return_type(**json.loads(res))
            except (JSONDecodeError, TypeError):
                return parse_error_message(res), None

        return wrapper

    return inner
