from functools import wraps


def strict(func):
    def check_type(arg_name, arg_val, expected_type):
        if type(arg_val) != expected_type:
            raise TypeError(f'Incorrect type {type(arg_val)} for {arg_name}, expected {expected_type}')

    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for i, (arg_name, arg_annotation) in enumerate(annotations.items()):
            if (len(args)) == i:
                break

            check_type(arg_name, args[i], arg_annotation)

        for (arg_name, arg_val) in kwargs.items():
            if arg_name not in annotations:
                raise TypeError(f'Unexpected argument {arg_name}')

            check_type(arg_name, arg_val, annotations[arg_name])

        return func(*args, **kwargs)

    return wrapper
