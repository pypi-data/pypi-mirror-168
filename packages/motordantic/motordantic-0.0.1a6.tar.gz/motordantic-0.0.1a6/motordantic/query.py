import copy
from json import dumps
from typing import Generator, List, Union, Any, Tuple, List, TYPE_CHECKING


__all__ = (
    "Query",
    "QueryCombination",
    "FindResult",
    "SimpleAggregateResult",
)


if TYPE_CHECKING:
    from .typing import MONGO_MODEL_TYPE


def _validate_query_data(model: 'MONGO_MODEL_TYPE', query: dict) -> dict:
    return model._validate_query_data(query)


class QueryNodeVisitor(object):
    """Base visitor class for visiting Query-object nodes in a query tree."""

    def prepare_combination(
        self, combination: 'QueryCombination'
    ) -> Union['QueryCombination', dict]:
        """Called by QueryCombination objects."""
        return combination

    def visit_query(self, query: 'Query') -> Union['Query', dict]:
        """Called by (New)Query objects."""
        return query


class SimplificationVisitor(QueryNodeVisitor):
    def __init__(self, model: 'MONGO_MODEL_TYPE'):
        self.model = model

    def prepare_combination(
        self, combination: 'QueryCombination'
    ) -> Union['QueryCombination', dict]:
        if combination.operation == combination.AND:
            # The simplification only applies to 'simple' queries
            if all(isinstance(node, Query) for node in combination.children):
                queries = [n.query for n in combination.children]
                query = self._query_conjunction(queries)
                return {"$and": query}

        return combination

    def _query_conjunction(self, queries):
        """Merges query dicts - effectively &ing them together."""
        combined_query = []
        for query in queries:
            query = _validate_query_data(self.model, query)
            combined_query.append(copy.deepcopy(query))
        return combined_query


class QueryCompilerVisitor(QueryNodeVisitor):
    """Compiles the nodes in a query tree to a PyMongo-compatible query
    dictionary.
    """

    def __init__(self, model: 'MONGO_MODEL_TYPE'):
        self.model = model

    def prepare_combination(
        self, combination: 'QueryCombination'
    ) -> Union['QueryCombination', dict]:
        operator = "$and"
        if combination.operation == combination.OR:
            operator = "$or"
        return {operator: combination.children}

    def visit_query(self, query: 'Query') -> Union['Query', dict]:
        data = _validate_query_data(self.model, query.query)
        return data


class QueryNode(object):
    """Base class for nodes in query trees."""

    AND = 0
    OR = 1

    def to_query(self, model: 'MONGO_MODEL_TYPE') -> dict:
        query = self.accept(SimplificationVisitor(model))
        if not isinstance(query, dict):
            query = query.accept(QueryCompilerVisitor(model))
        return query

    def accept(self, visitor):
        raise NotImplementedError

    def _combine(self, other, operation):
        """Combine this node with another node into a QueryCombination
        object.
        """
        # If the other Query() is empty, ignore it and just use `self`.
        if getattr(other, "empty", True):
            return self

        # Or if this Q is empty, ignore it and just use `other`.
        if self.empty:
            return other

        return QueryCombination(operation, [self, other])

    @property
    def empty(self):
        return False

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)


class QueryCombination(QueryNode):
    def __init__(self, operation, children):
        self.operation = operation
        self.children = []
        for node in children:
            # If the child is a combination of the same type, we can merge its
            # children directly into this combinations children
            if isinstance(node, QueryCombination) and node.operation == operation:
                self.children += node.children
            else:
                self.children.append(node)

    def __repr__(self):
        op = " & " if self.operation is self.AND else " | "
        return "(%s)" % op.join([repr(node) for node in self.children])

    def __bool__(self):
        return bool(self.children)

    def accept(self, visitor) -> Union['QueryCombination', dict]:
        for i in range(len(self.children)):
            if isinstance(self.children[i], QueryNode):
                self.children[i] = self.children[i].accept(visitor)

        return visitor.prepare_combination(self)

    @property
    def empty(self):
        return not bool(self.children)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.operation == other.operation
            and self.children == other.children
        )


class Query(QueryNode):
    """A simple query object, used in a query tree to build up more complex
    query structures.
    """

    def __init__(self, **query):
        self.query = query

    def __repr__(self):
        return "Query(**%s)" % repr(self.query)

    def __bool__(self):
        return bool(self.query)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.query == other.query

    def accept(self, visit: 'QueryNodeVisitor') -> Union['Query', dict]:
        return visit.visit_query(self)

    @property
    def empty(self) -> bool:
        return not bool(self.query)


class FindResult(object):
    __slots__ = ('_data', 'mongo_model_class')

    def __init__(
        self,
        mongo_model_class: 'MONGO_MODEL_TYPE',
        data: list,
    ):
        self._data = data
        self.mongo_model_class = mongo_model_class

    # @handle_and_convert_connection_errors
    def __iter__(self):
        for obj in self._data:
            yield obj

    def __next__(self):
        return next(self.__iter__())

    @property
    def data(self) -> List:
        return [obj.data for obj in self.__iter__()]

    @property
    def generator(self) -> Generator:
        return self.__iter__()

    @property
    def data_generator(self) -> Generator:
        for obj in self.__iter__():
            yield obj.data

    @property
    def list(self) -> List:
        return list(self.__iter__())

    def json(self) -> str:
        return dumps(self.data)

    def first(self) -> Any:
        return next(self.__iter__())

    def serialize(
        self, fields: Union[Tuple, List], to_list: bool = True
    ) -> Union[Tuple, List]:
        return (
            [obj.serialize(fields) for obj in self.__iter__()]
            if to_list
            else tuple(obj.serialize(fields) for obj in self.__iter__())
        )

    def serialize_generator(self, fields: Union[Tuple, List]) -> Generator:
        for obj in self.__iter__():
            yield obj.serialize(fields)

    def serialize_json(self, fields: Union[Tuple, List]) -> str:
        return dumps(self.serialize(fields))


class SimpleAggregateResult(object):
    __slots__ = ('_data', 'mongo_model_class')

    def __init__(
        self,
        mongo_model_class: 'MONGO_MODEL_TYPE',
        data: dict,
    ):
        self._data = data
        self.mongo_model_class = mongo_model_class

    def json(self) -> str:
        return dumps(self._data)

    @property
    def data(self) -> dict:
        return self._data
