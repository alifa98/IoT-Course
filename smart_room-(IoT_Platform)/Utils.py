# this decorator catches and handles all exceptions
from functools import wraps
import json
import string
from CustomError import CustomError


def catch_all_exceptions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as e:
            return create_response(False, {"reason": e.message})
        except Exception as e:
            return create_response(False, {"reason": e.__class__.__name__})
    return decorated_function


def check_empty_error(input_value, key="an input"):
    if (input_value is string and not input_value.strip()) or (not input_value):
        raise CustomError(key + " is empty")

    return input_value


def create_response(is_successful: bool, data={}):
    return json.dumps({"status": "success" if is_successful else "error"} | data)
