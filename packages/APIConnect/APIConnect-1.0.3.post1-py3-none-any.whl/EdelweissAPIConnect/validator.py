from datetime import datetime
import functools
import inspect
import logging
from exceptions.validation_exception import ValidationException

LOGGER = logging.getLogger(__name__)

class Validator:

    # validation decorator
    @staticmethod
    def ValidateInputDataTypes(func):
        @functools.wraps(func)
        def validate(*args, **kwargs):
            # a mapping of variable names from the function definition and the values given at function call time
            variables_value_map = dict(inspect.signature(func).bind(*args, **kwargs).arguments)

            # a mapping of variables and their type annotations provided in function defintion
            for variable, type_annotation in func.__annotations__.items():
                if variable not in variables_value_map.keys():
                    # if some option variable is not given a value at function call time, skip its type checking
                    continue
                if type_annotation in [None, True, False]:
                    type_annotation = type(type_annotation)
                if not isinstance(variables_value_map[variable], type_annotation):
                    exc = ValidationException(f"Function {func.__name__} : {variable} is a not a valid {type_annotation} type.")
                    LOGGER.exception(exc)
                    raise exc
            return func(*args, **kwargs)
        return validate

    # isRequired decorator
    @staticmethod
    def isRequired(required=None):
        '''
        Parameters :
        `required` : Name of parameter as a string | List of strings of parameter names
        '''
        def is_none_or_empty_test(func, args_dict, required):
            has_none_is_empty = False
            bad_parameters = []

            for param, value in args_dict.items():
                if param in list(required):
                    if isinstance(value, str):
                        value = value.strip()
                    try:
                        len(value)
                    except TypeError as e:
                        # TypeError if value is of type <int/float or None or something else> - numerics are currently allowed to be 0
                        if value is None:
                            bad_parameters.append(param)
                            has_none_is_empty = True
                    else:
                        if not len(value):
                            # checks for empty <strings, dicts, lists, tuples>
                            bad_parameters.append(param)
                            has_none_is_empty = True

            if has_none_is_empty:
                exc = ValidationException(
                    f'function {func.__name__}: Parameters {bad_parameters} cannot be None or Empty.')
                LOGGER.exception(exc)
                raise exc

        def real_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                variables_value_map = dict(
                    zip(inspect.signature(func).parameters, args+tuple(kwargs.values())))
                is_none_or_empty_test(func, variables_value_map, required)
                return func(*args, **kwargs)
            return wrapper
        return real_decorator

    @staticmethod
    def isRequiredv2(name, value):

        has_none_is_empty = False

        if isinstance(value, str):
            value = value.strip()
        try:
            len(value)
        except TypeError as e:
            # TypeError if value is of type <int/float or None or something else> - numerics are currently allowed to be 0
            if value is None:
                has_none_is_empty = True
        else:
            if not len(value):
                # checks for empty <strings, dicts, lists, tuples>
                has_none_is_empty = True

        if has_none_is_empty:
            exc = ValidationException(f'Parameter {name} cannot be None or Empty.')
            LOGGER.exception(exc)
            raise exc

        return value

    @staticmethod
    def validate_datetime_format(date_time_string, pattern) :
        try:
            datetime.strptime(date_time_string, pattern)
        except ValueError as e:
            exc = ValidationException(e.args[0])
            LOGGER.exception(exc)
            raise exc