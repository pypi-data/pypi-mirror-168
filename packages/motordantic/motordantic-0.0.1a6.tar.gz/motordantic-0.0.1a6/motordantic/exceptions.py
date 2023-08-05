from time import sleep
from types import GeneratorType
from typing import Callable, Any

from pymongo.errors import (
    ServerSelectionTimeoutError,
    AutoReconnect,
    NetworkTimeout,
    ConnectionFailure,
)


class BaseMotorDanticException(Exception):
    pass


class NotDeclaredField(BaseMotorDanticException):
    def __init__(self, field_name: str, fields: list, *args):
        self.field_name = field_name
        self.fields = fields
        super().__init__(*args)

    def __str__(self):
        return f"This field - {self.field_name} not declared in {self.fields}"


class DoesNotExist(BaseMotorDanticException):
    def __init__(self, model_name: str, *args):
        super().__init__(args)
        self.model_name = model_name

    def __str__(self):
        return f'row does not exist for model: {self.model_name}'


class MotordanticValidationError(BaseMotorDanticException):
    pass


class MotordanticInvalidArgsParams(BaseMotorDanticException):
    def __str__(self):
        return 'Arguments must be Query objects'


class MotordanticConnectionError(BaseMotorDanticException):
    pass


class MotordanticIndexError(BaseMotorDanticException):
    pass


def handle_and_convert_connection_errors(func: Callable) -> Any:
    """decorator for handle connection errors and raise MongoConnectionError

    Args:
        func (Callable):any query to mongo

    Returns:
        Any: data
    """

    def generator_wrapper(generator):
        yield from generator

    def main_wrapper(*args, **kwargs):
        counter = 1
        while True:
            try:
                result = func(*args, **kwargs)
                if isinstance(result, GeneratorType):
                    result = generator_wrapper(result)
                return result
            except (
                AutoReconnect,
                ServerSelectionTimeoutError,
                NetworkTimeout,
                ConnectionFailure,
            ) as e:
                counter += 1
                if counter > 3:
                    raise MotordanticConnectionError(str(e))
                sleep(counter)

    return main_wrapper
