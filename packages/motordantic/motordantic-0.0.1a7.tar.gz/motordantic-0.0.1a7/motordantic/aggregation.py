from typing import TYPE_CHECKING

from .exceptions import MotordanticValidationError

if TYPE_CHECKING:
    from .models import MongoModel


__all__ = ('Sum', 'Avg', 'Min', 'Count', 'Max')


class BaseAggregation(object):
    """Abstract class for Aggregation"""

    __slots__ = ('field', '_operation')

    _operation: str

    def __init__(self, field: str):
        self.field = field

    @property
    def operation(self) -> str:
        if not self._operation:
            raise NotImplementedError('implement _operation')
        return self._operation

    def _validate_field(self, mongo_model_class: 'MongoModel'):
        if self.field not in mongo_model_class.__fields__ and self.field != '_id':
            raise MotordanticValidationError(
                f'invalid field "{self.field}" for this model, field must be one of {list(mongo_model_class.__fields__.keys())}'
            )

    def _aggregate_query(self, mongo_model_class: 'MongoModel') -> dict:
        self._validate_field(mongo_model_class)
        query = {
            f'{self.field}__{self.operation}': {f'${self.operation}': f'${self.field}'}
        }
        return query


class Sum(BaseAggregation):
    """
    Simple sum aggregation

    generated query: {'field__sum': {'$sum': 'field'}}

    return: {'field__sum': <value>}
    """

    _operation: str = 'sum'


class Max(BaseAggregation):
    """
    Simple max aggregation

    generated query: {'field__max': {'$max': 'field'}}

    return: {'field__max': <value>}
    """

    _operation: str = 'max'


class Min(BaseAggregation):
    """
    Simple min aggregation

    generated query: {'field__min': {'$min': 'field'}}

    return: {'field__min': <value>}
    """

    _operation: str = 'min'


class Avg(BaseAggregation):
    """
    Simple avg aggregation

    generated query: {'field__avg': {'$avg': 'field'}}

    return: {'field__avg': <value>}
    """

    _operation: str = 'avg'


class Count(BaseAggregation):
    """
    Simple Count aggregation

    generated query:
        - if field = _id
            {
                '_id': None
                'count': {'$sum': 1},
            }
        - else
            {
                '_id': 'field'
                'count': {'$sum': 1},
            }
    return: {'_id': <value>, 'count': value}
    """

    _operation: str = 'count'

    def _aggregate_query(self, mongo_model_class: 'MongoModel') -> dict:
        self._validate_field(mongo_model_class)
        query = {
            "_id": f'${self.field}' if self.field != '_id' else None,
            f'count': {'$sum': 1},
        }
        return query
