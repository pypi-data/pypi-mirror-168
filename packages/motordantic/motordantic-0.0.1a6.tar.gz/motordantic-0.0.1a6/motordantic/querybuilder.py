import asyncio
import os
from typing import (
    AsyncIterable,
    Union,
    List,
    Dict,
    Optional,
    Any,
    Tuple,
    TYPE_CHECKING,
    Iterable,
    Type,
    no_type_check,
)

from bson import ObjectId
from pymongo import ReturnDocument, IndexModel
from motor.core import AgnosticClientSession as ClientSession


from .query import Query, QueryCombination, FindResult, SimpleAggregateResult
from .connection import _connections
from .validaton import sort_validation
from .exceptions import DoesNotExist, MotordanticValidationError, MotordanticIndexError
from .aggregation import Sum, Max, Min, Avg
from .extra import (
    generate_name_field,
    group_by_aggregate_generation,
    bulk_query_generator,
    chunk_by_length,
)

__all__ = ('QueryBuilder',)

if TYPE_CHECKING:
    from .models import MongoModel


MONGO_MODEL_TYPE = Type['MongoModel']


class QueryBuilder(object):
    __slots__ = ('mongo_model_class', 'motor_client', '_io_loop')

    def __init__(self, mongo_model_class: MONGO_MODEL_TYPE):
        self.mongo_model_class: MONGO_MODEL_TYPE = mongo_model_class
        if self.mongo_model_class.__database__ is None:
            if not _connections:
                raise RuntimeError('not `connect` called.')
            connection = _connections[os.getenv('MOTORDANTIC_ENV_NAME') or 'default']
            motor_client = connection._get_motor_client()
            mongo_model_class.use(motor_client.get_database(connection.db_name))
            self.motor_client = motor_client
        else:
            self.motor_client = self.mongo_model_class.__database__.client

    @property
    def sync(self) -> "SyncQueryBuilder":
        s = SyncQueryBuilder(self.mongo_model_class)
        return s

    async def _make_query(
        self,
        method_name: str,
        query_params: Union[List, Dict, str, Query, QueryCombination],
        set_values: Optional[Dict] = None,
        session: Optional[ClientSession] = None,
        logical: bool = False,
        **kwargs,
    ) -> Any:
        """main query function

        Args:
            method_name (str): query method like find, find_one and other
            query_params (Union[List, Dict, str, Query, LogicalCombination]): query params: dict or Query or LogicalCombination
            set_values (Optional[Dict], optional): for updated method. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.
            logical (bool, optional): if logical. Defaults to False.

        Returns:
            Any: query result
        """
        if logical:
            query_params = self.mongo_model_class._check_query_args(query_params)
        elif isinstance(query_params, dict):
            query_params = self.mongo_model_class._validate_query_data(query_params)
        method = getattr(self.mongo_model_class.collection, method_name)
        query: tuple = (query_params,)
        if session:
            kwargs['session'] = session
        if set_values:
            query = (query_params, set_values)
        if kwargs:
            return await method(*query, **kwargs)
        return await method(*query)

    async def count(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        """count query

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query | QueryCombination. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: count of documents
        """
        if getattr(self.mongo_model_class.collection, 'count_documents'):
            return await self._make_query(
                'count_documents',
                logical_query or query,
                session=session,
                logical=bool(logical_query),
            )
        return await self._make_query(
            'count',
            logical_query or query,
            session=session,
            logical=bool(logical_query),
        )

    async def count_documents(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        """count_documents query

        Args:
            logical_query (Union[Query, LogicalCombination, None], optional): Query | QueryCombination. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: count of documents
        """
        return await self.count(logical_query, session, **query)

    async def insert_one(
        self, session: Optional[ClientSession] = None, **query
    ) -> ObjectId:
        """insert one document

        Args:
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            ObjectId: created document _id
        """
        obj = self.mongo_model_class.parse_obj(query)
        data = await self._make_query('insert_one', obj._query_data, session=session)
        return data.inserted_id

    async def insert_many(
        self, data: List, session: Optional[ClientSession] = None
    ) -> int:
        """insert many documents

        Args:
            data (List): List of dict or MongoModels
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: count inserted ids
        """
        parse_obj = self.mongo_model_class.parse_obj
        query = [
            parse_obj(obj)._query_data if isinstance(obj, dict) else obj._query_data
            for obj in data
        ]
        r = await self._make_query('insert_many', query, session=session)
        return len(r.inserted_ids)

    async def delete_one(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        """delete one document

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query|QueryCombination. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: deleted documents count
        """
        r = await self._make_query(
            'delete_one',
            logical_query or query,
            session=session,
            logical=bool(logical_query),
        )
        return r.deleted_count

    async def delete_many(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        """delete many document

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query|QueryCombination. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: deleted documents count
        """
        r = await self._make_query(
            'delete_many',
            logical_query or query,
            session=session,
            logical=bool(logical_query),
        )
        return r.deleted_count

    async def list_indexes(self, session: Optional[ClientSession] = None) -> dict:
        """get indexes for this collection

        Returns:
            dict: indexes result
        """
        list_indexes_cursor = getattr(self.mongo_model_class.collection, 'list_indexes')
        query = list_indexes_cursor(session=session)
        index_list = await query.to_list(None)
        return_data = {}
        for index in index_list:
            dict_index = dict(index)
            data = {dict_index['name']: {'key': dict(dict_index['key'])}}
            return_data.update(data)
        return return_data

    async def create_indexes(
        self,
        indexes: List[IndexModel],
        session: Optional[ClientSession] = None,
    ) -> List[str]:
        create_indexes_cursor = getattr(
            self.mongo_model_class.collection, 'create_indexes'
        )
        return await create_indexes_cursor(
            indexes,
            session=session,
            maxTimeMS=3600,
        )

    async def drop_index(
        self, index_name: str, session: Optional[ClientSession] = None
    ) -> str:
        indexes = await self.list_indexes(session)
        if index_name in indexes:
            await self._make_query('drop_index', index_name, session=session)
            return f'{index_name} dropped.'
        raise MotordanticIndexError(f'invalid index name - {index_name}')

    async def _find(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        skip_rows: Optional[int] = None,
        limit_rows: Optional[int] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        **query,
    ) -> AsyncIterable:
        sort, sort_fields_parsed = sort_validation(sort, sort_fields)

        async def context():
            if bool(logical_query):
                query_params = self.mongo_model_class._check_query_args(logical_query)
            else:
                query_params = self.mongo_model_class._validate_query_data(query)
            find_cursor_method = getattr(self.mongo_model_class.collection, 'find')
            cursor = find_cursor_method(query_params, session=session)
            if skip_rows is not None:
                cursor = cursor.skip(skip_rows)
            if limit_rows:
                cursor = cursor.limit(limit_rows)
            if sort:
                cursor.sort([(field, sort or 1) for field in sort_fields_parsed])
            async for doc in cursor:
                yield self.mongo_model_class.parse_obj(doc)

        return context()

    async def find(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        skip_rows: Optional[int] = None,
        limit_rows: Optional[int] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> FindResult:
        """find method

        Args:
            logical_query (Union[Query, LogicalCombination, None], optional): Query|LogicalCombunation. Defaults to None.
            skip_rows (Optional[int], optional): skip rows for pagination. Defaults to None.
            limit_rows (Optional[int], optional): limit rows. Defaults to None.
            session (Optional[ClientSession], optional): pymongo session. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): iterable from sort fielda. Defaults to None.
            sort (Optional[int], optional): sort value -1 or 1. Defaults to None.

        Returns:
            FindResult: Motordantic FindResult
        """
        result = await self._find(
            logical_query, skip_rows, limit_rows, session, sort_fields, sort, **query
        )
        data = [doc async for doc in result]
        if with_relations_objects and self.mongo_model_class.relation_manager:
            data = await self.mongo_model_class.relation_manager.map_relation_for_array(
                data
            )
        return FindResult(self.mongo_model_class, data)

    async def find_with_count(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        skip_rows: Optional[int] = None,
        limit_rows: Optional[int] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        **query,
    ) -> Tuple[int, FindResult]:
        """find and count

        Args:
            logical_query (Union[Query, LogicalCombination, None], optional): Query|QueryCombination or None. Defaults to None.
            skip_rows (Optional[int], optional): for pagination. Defaults to None.
            limit_rows (Optional[int], optional): for pagination. Defaults to None.
            session (Optional[ClientSession], optional): pymongo session. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): field for sort. Defaults to None.
            sort (Optional[int], optional): sort value. Defaults to None.

        Returns:
            Tuple[int, FindResult]: count of query data, FindResult
        """
        count = await self.count(
            session=session,
            logical_query=logical_query,
            **query,
        )
        results = await self.find(
            skip_rows=skip_rows,
            limit_rows=limit_rows,
            session=session,
            logical_query=logical_query,
            sort_fields=sort_fields,
            sort=sort,
            **query,
        )
        return count, results

    async def find_one(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        session: Optional[ClientSession] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> Optional['MongoModel']:
        """find one document

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query | LogicalCombination. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): iterable from sort fielda. Defaults to None.
            sort (Optional[int], optional): sort value -1 or 1. Defaults to None.

        Returns:
            Optional[MongoModel]: MongoModel instance or None
        """
        sort, sort_fields = sort_validation(sort, sort_fields)
        data = await self._make_query(
            'find_one',
            logical_query or query,
            logical=bool(logical_query),
            sort=[(field, sort or 1) for field in sort_fields] if sort_fields else None,
            session=session,
        )
        if data:
            obj = self.mongo_model_class.parse_obj(data)
            if with_relations_objects and self.mongo_model_class.relation_manager:
                obj = await self.mongo_model_class.relation_manager.map_relation_for_single(
                    obj
                )
            return obj
        return None

    def _prepare_update_data(self, **fields) -> tuple:
        """prepare and validate query data for update queries"""

        if not any("__set" in f for f in fields):
            raise MotordanticValidationError("not fields for updating!")
        query_params = {}
        set_values = {}
        for name, value in fields.items():
            if name.endswith('__set'):
                name = name.replace('__set', '')
                data = self.mongo_model_class._validate_query_data({name: value})
                set_values.update(data)
            else:
                query_params.update({name: value})
        return query_params, set_values

    async def replace_one(
        self,
        replacement: Dict,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **filter_query,
    ) -> Any:
        """replace one

        Args:
            replacement (Dict): replacement object
            upsert (bool, optional): pymongo upsert. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Raises:
            MotordanticValidationError: if not filter query
            MotordanticValidationError: if not replacement obj

        Returns:
            Any: pymongo replace_one query result
        """
        if not filter_query:
            raise MotordanticValidationError('not filter parameters')
        if not replacement:
            raise MotordanticValidationError('not replacement parameters')
        return await self._make_query(
            'replace_one',
            self.mongo_model_class._validate_query_data(filter_query),
            replacement=self.mongo_model_class._validate_query_data(replacement),
            upsert=upsert,
            session=session,
        )

    async def get(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> Any:
        """method like django orm get

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query objects. Defaults to None.
            session (Optional[ClientSession], optional): mongo session. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): sorts. Defaults to None.
            sort (Optional[int], optional): sort. Defaults to None.

        Raises:
            DoesNotExist: raise if not found object

        Returns:
            Any: mongo model
        """

        obj = await self.find_one(
            logical_query=logical_query,
            session=session,
            sort_fields=sort_fields,
            sort=sort,
            **query,
        )
        if not obj:
            raise DoesNotExist(self.mongo_model_class.__name__)  # type: ignore
        if with_relations_objects and self.mongo_model_class.relation_manager:
            obj = await self.mongo_model_class.relation_manager.map_relation_for_single(
                obj
            )
        return obj

    async def get_or_create(self, **query) -> Tuple:
        """like django orm get_or_create

        Returns:
            Tuple: MongoModel instance, True/False
        """
        defaults = query.pop('defaults', {})
        with_relations_objects = query.pop('with_relations_objects', False)
        obj = await self.find_one(
            **query, with_relations_objects=with_relations_objects
        )
        if obj:
            created = False
        else:
            created = True
            inserted_id = await self.insert_one(**{**query, **defaults})
            obj = await self.find_one(
                _id=inserted_id, with_relations_objects=with_relations_objects
            )
        return obj, created

    async def update_or_create(self, **query) -> Tuple:
        """like django orm update_or_create

        Returns:
            Tuple: MongoModel instance, True/False
        """
        defaults = query.pop('defaults', {})
        with_relations_objects = query.pop('with_relations_objects', False)
        obj = await self.find_one(
            **query, with_relations_objects=with_relations_objects
        )
        if obj is not None:
            created = False
            for field, value in defaults.items():
                setattr(obj, field, value)
        else:
            created = True
            obj = self.mongo_model_class(**{**query, **defaults})  # type: ignore
        await obj.save()
        if with_relations_objects:
            obj = await self.get(
                _id=obj._id, with_relations_objects=with_relations_objects
            )
        return obj, created

    def _validate_raw_query(
        self, method_name: str, raw_query: Union[Dict, List[Dict], Tuple[Dict]]
    ) -> tuple:
        if (
            'insert' in method_name
            or 'replace' in method_name
            or 'update' in method_name
        ):
            if isinstance(raw_query, list):
                raw_query = list(
                    map(self.mongo_model_class._validate_query_data, raw_query)
                )
            elif isinstance(raw_query, dict):
                raw_query = self.mongo_model_class._validate_query_data(raw_query)
            else:
                params = [
                    query[key] if '$' in key else query
                    for query in raw_query
                    for key in query.keys()
                ]
                map(self.mongo_model_class._validate_query_data, params)
        parsed_query = raw_query if isinstance(raw_query, tuple) else (raw_query,)
        return parsed_query

    async def raw_query(
        self,
        method_name: str,
        raw_query: Union[Dict, List[Dict], Tuple[Dict]],
        session: Optional[ClientSession] = None,
    ) -> Any:
        """pymongo raw query

        Args:
            method_name (str): pymongo method, like insert_one
            raw_query (Union[Dict, List[Dict], Tuple[Dict]]): query data
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Raises:
            MongoValidationError: raise if invalid data

        Returns:
            Any: pymongo query result
        """
        parsed_query = self._validate_raw_query(method_name, raw_query)
        try:
            query = getattr(self.mongo_model_class.collection, method_name)
            return await query(*parsed_query, session=session)
        except AttributeError:
            raise MotordanticValidationError('invalid method name')

    async def _update(
        self,
        method: str,
        query: Dict,
        upsert: bool = True,
        session: Optional[ClientSession] = None,
    ) -> int:
        """innert method for update

        Args:
            method (str): one of update_many or update_one
            query (Dict): update query
            upsert (bool, optional): upsert option. Defaults to True.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: updated documents count
        """
        query, set_values = self._prepare_update_data(**query)
        r = await self._make_query(
            method, query, {'$set': set_values}, upsert=upsert, session=session
        )
        return r.modified_count

    async def update_one(
        self, upsert: bool = False, session: Optional[ClientSession] = None, **query
    ) -> int:
        """update one document

        Args:
            upsert (bool, optional): pymongo upsert. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: updated documents count
        """
        return await self._update('update_one', query, upsert=upsert, session=session)

    async def update_many(
        self, upsert: bool = False, session: Optional[ClientSession] = None, **query
    ) -> int:
        """update many document

        Args:
            upsert (bool, optional): pymongo upsert. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: updated documents count
        """
        return await self._update('update_many', query, upsert=upsert, session=session)

    async def distinct(
        self, field: str, session: Optional[ClientSession] = None, **query
    ) -> list:
        """wrapper for pymongo distinct

        Args:
            field (str): distinct field
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            list: list of distinct values
        """
        query = self.mongo_model_class._validate_query_data(query)
        method = getattr(self.mongo_model_class.collection, 'distinct')
        return await method(key=field, filter=query, session=session)

    async def raw_aggregate(
        self, data: List[Dict[Any, Any]], session: Optional[ClientSession] = None
    ) -> list:
        """raw aggregation query

        Args:
            data (List[Dict[Any, Any]]): aggregation query
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            list: aggregation result
        """
        result = await self._motor_aggreggate_call(data, session)
        return [row async for row in result]

    async def _motor_aggreggate_call(
        self, data: list, session: Optional[ClientSession]
    ) -> AsyncIterable:
        async def context():
            aggregate_cursor = getattr(self.mongo_model_class.collection, 'aggregate')

            async for row in aggregate_cursor(data, session=session):
                yield row

        return context()

    async def _aggregate(self, *args, **query) -> SimpleAggregateResult:
        """main aggregate method

        Raises:
            MongoValidationError: miss aggregation or group_by

        Returns:
            dict: aggregation result
        """
        session = query.pop('session', None)
        aggregation = query.pop('aggregation', None)
        group_by = query.pop('group_by', None)
        if not aggregation and not group_by:
            raise MotordanticValidationError('miss aggregation or group_by')
        if isinstance(aggregation, Iterable):
            aggregate_query = {}
            for agg in aggregation:
                aggregate_query.update(agg._aggregate_query(self.mongo_model_class))
        elif aggregation is not None:
            aggregate_query = aggregation._aggregate_query(self.mongo_model_class)
        else:
            aggregate_query = {}
        if group_by:
            group_by = group_by_aggregate_generation(group_by)
            aggregate_query.pop('_id', None)
            group_params = {"$group": {"_id": group_by, **aggregate_query}}
        else:
            group_params = {
                "$group": {"_id": None, **aggregate_query}
                if '_id' not in aggregate_query
                else aggregate_query
            }
        data = [
            {
                "$match": self.mongo_model_class._validate_query_data(query)
                if not args
                else self.mongo_model_class._check_query_args(*args)
            },
            group_params,
        ]

        async_result = await self._motor_aggreggate_call(data, session)
        result = [row async for row in async_result]
        if not result:
            return SimpleAggregateResult(self.mongo_model_class, {})
        result_data = {}
        for r in result:
            name = generate_name_field(r.pop('_id'))
            result_data.update({name: r} if name else r)
        return SimpleAggregateResult(self.mongo_model_class, result_data)

    async def simple_aggregate(self, *args, **kwargs) -> SimpleAggregateResult:
        return await self._aggregate(*args, **kwargs)

    async def aggregate_sum(self, agg_field: str, **query) -> Union[int, float]:
        result = await self._aggregate(aggregation=Sum(agg_field), **query)
        return result.data.get(f'{agg_field}__sum', 0)

    async def aggregate_max(self, agg_field: str, **query) -> Union[int, float]:
        result = await self._aggregate(aggregation=Max(agg_field), **query)
        return result.data.get(f'{agg_field}__max', 0)

    async def aggregate_min(self, agg_field: str, **query) -> Union[int, float]:
        result = await self._aggregate(aggregation=Min(agg_field), **query)
        return result.data.get(f'{agg_field}__min', 0)

    async def aggregate_avg(self, agg_field: str, **query) -> Union[int, float]:
        result = await self._aggregate(aggregation=Avg(agg_field), **query)
        return result.data.get(f'{agg_field}__avg', 0)

    async def _bulk_operation(
        self,
        models: List,
        updated_fields: Optional[List] = None,
        query_fields: Optional[List] = None,
        batch_size: Optional[int] = 10000,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
    ) -> None:
        """base bulk operation method

        Args:
            models (List): MongoModels objects
            updated_fields (Optional[List], optional): list of updated fields. Defaults to None.
            query_fields (Optional[List], optional): list of query fields. Defaults to None.
            batch_size (Optional[int], optional): query batch. Defaults to 10000.
            upsert (bool, optional): for upsert pymongo queries. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.
        """
        if batch_size is not None and batch_size > 0:
            for requests in chunk_by_length(models, batch_size):
                data = bulk_query_generator(
                    requests,
                    updated_fields=updated_fields,
                    query_fields=query_fields,
                    upsert=upsert,
                )
                await self._make_query('bulk_write', data, session=session)
            return None
        data = bulk_query_generator(
            models,
            updated_fields=updated_fields,
            query_fields=query_fields,
            upsert=upsert,
        )
        await self._make_query('bulk_write', data, session=session)

    async def bulk_update(
        self,
        models: List,
        updated_fields: List,
        batch_size: Optional[int] = None,
        session: Optional[ClientSession] = None,
    ) -> None:
        """bulk update method

        Args:
            models (List): MongoModel objects
            updated_fields (List): list of updated fields, like ['name', 'last_name']
            batch_size (Optional[int], optional): query batch. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Raises:
            MongoValidationError: if invalid param
        """
        if not updated_fields:
            raise MotordanticValidationError('updated_fields cannot be empty')
        await self._bulk_operation(
            models,
            updated_fields=updated_fields,
            batch_size=batch_size
            if batch_size is not None and batch_size > 0
            else 10000,
            session=session,
        )

    async def bulk_create(
        self,
        models: List,
        batch_size: Optional[int] = 30000,
        session: Optional[ClientSession] = None,
    ) -> int:
        """bulk create method

        Args:
            models (List): MongoModels obejcts
            batch_size (Optional[int], optional): query batch. Defaults to None.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            int: count of objects created
        """
        if batch_size is None or batch_size <= 0:
            batch_size = 30000
        result = 0
        for data in chunk_by_length(models, batch_size):
            inserted_count = await self.insert_many(data, session=session)
            result += inserted_count
        return result

    async def bulk_update_or_create(
        self,
        models: List,
        query_fields: List,
        batch_size: Optional[int] = 10000,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Method for update/create rows

        Args:
            models (List): List of MongoModels objects
            query_fields (List): list of query fields like ['name'], perfect if this fields in indexes
            batch_size (Optional[int], optional): query obejcts batch. Defaults to 10000.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Raises:
            MongoValidationError: if invalid models

        """
        if not query_fields:
            raise MotordanticValidationError('query_fields cannot be empty')
        return await self._bulk_operation(
            models,
            query_fields=query_fields,
            batch_size=batch_size,
            upsert=True,
            session=session,
        )

    async def _find_with_replacement_or_with_update(
        self,
        operation: str,
        projection_fields: Optional[list] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **query,
    ) -> Union[Dict, 'MongoModel', None]:
        """base method for find_with_<operation>

        Args:
            operation (str): operation name
            projection_fields (Optional[list], optional): prejection. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): sort fields. Defaults to None.
            sort (Optional[int], optional): -1 or 1. Defaults to None.
            upsert (bool, optional): True/False. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            Union[Dict, 'MongoModel']: MongoModel or Dict
        """
        filter_, set_values = self._prepare_update_data(**query)
        return_document = ReturnDocument.AFTER
        replacement = query.pop('replacement', None)

        projection = {f: True for f in projection_fields} if projection_fields else None
        extra_params = {
            'return_document': return_document,
            'projection': projection,
            'upsert': upsert,
            'session': session,
        }
        if sort_fields:
            extra_params['sort'] = [(field, sort or 1) for field in sort_fields]

        if replacement:
            extra_params['replacement'] = replacement

        data = await self._make_query(
            operation, filter_, set_values={'$set': set_values}, **extra_params
        )
        if projection:
            return {
                field: value for field, value in data.items() if field in projection
            }
        if data:
            return self.mongo_model_class.parse_obj(data)
        return None

    async def find_one_and_update(
        self,
        projection_fields: Optional[list] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **query,
    ) -> Union[Dict, 'MongoModel', None]:
        """find one and update

        Args:
            operation (str): operation name
            projection_fields (Optional[list], optional): prejection. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): sort fields. Defaults to None.
            sort (Optional[int], optional): -1 or 1. Defaults to None.
            upsert (bool, optional): True/False. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            Union[Dict, 'MongoModel']: MongoModel or Dict
        """
        return await self._find_with_replacement_or_with_update(
            'find_one_and_update',
            projection_fields=projection_fields,
            sort_fields=[(field, sort or 1) for field in sort_fields]
            if sort_fields
            else None,
            sort=sort,
            upsert=upsert,
            session=session,
            **query,
        )

    async def find_and_replace(
        self,
        replacement: Union[dict, Any],
        projection_fields: Optional[list] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **query,
    ) -> Union[Dict, 'MongoModel', None]:
        """find one and replace

        Args:
            operation (str): operation name
            projection_fields (Optional[list], optional): prejection. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): sort fields. Defaults to None.
            sort (Optional[int], optional): -1 or 1. Defaults to None.
            upsert (bool, optional): True/False. Defaults to False.
            session (Optional[ClientSession], optional): motor session. Defaults to None.

        Returns:
            Union[Dict, 'MongoModel']: MongoModel or Dict
        """
        if not isinstance(replacement, dict):
            replacement = replacement.query_data
        return await self._find_with_replacement_or_with_update(
            'find_and_replace',
            projection_fields=projection_fields,
            sort_fields=[(field, sort) for field in sort_fields]
            if sort_fields
            else None,
            sort=sort,
            upsert=upsert,
            session=session,
            replacement=replacement,
            **query,
        )

    async def drop_collection(self, force: bool = False) -> bool:
        """drop collection

        Args:
            force (bool, optional): if u wanna force drop. Defaults to False.

        Returns:
            bool: result message
        """
        if force:
            await self._make_query('drop', query_params={})
            return True
        value = input(
            f'Are u sure for drop this collection - {self.mongo_model_class.__name__.lower()} (y, n)'  # type: ignore
        )
        if value.lower() == 'y':
            await self._make_query('drop', query_params={})
            return True
        return False


class SyncQueryBuilder(QueryBuilder):
    def __init__(self, mongo_model_class: MONGO_MODEL_TYPE):
        super().__init__(mongo_model_class)
        try:
            self._io_loop = (
                self.motor_client.io_loop
                if self.motor_client.io_loop is not None
                else asyncio.get_running_loop()
            )
        except RuntimeError:
            self._io_loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(self._io_loop)

    @property
    def sync(self):
        raise AttributeError('cant call call in sync builder.')

    @no_type_check
    def insert_one(self, session: Optional[ClientSession] = None, **query) -> ObjectId:
        return self._io_loop.run_until_complete(super().insert_one(session, **query))

    @no_type_check
    def insert_many(self, data: List, session: Optional[ClientSession] = None) -> int:
        return self._io_loop.run_until_complete(super().insert_many(data, session))

    @no_type_check
    def find_one(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        session: Optional[ClientSession] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> Optional['MongoModel']:
        return self._io_loop.run_until_complete(
            super().find_one(
                logical_query,
                sort_fields,
                session,
                sort,
                with_relations_objects,
                **query,
            )
        )

    @no_type_check
    def find(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        skip_rows: Optional[int] = None,
        limit_rows: Optional[int] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> FindResult:
        return self._io_loop.run_until_complete(
            super().find(
                logical_query,
                skip_rows,
                limit_rows,
                session,
                sort_fields,
                sort,
                with_relations_objects,
                **query,
            )
        )

    @no_type_check
    def delete_one(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        return self._io_loop.run_until_complete(
            super().delete_one(logical_query, session, **query)
        )

    @no_type_check
    def delete_many(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        return self._io_loop.run_until_complete(
            super().delete_many(logical_query, session, **query)
        )

    @no_type_check
    def update_many(
        self, upsert: bool = False, session: Optional[ClientSession] = None, **query
    ) -> int:
        return self._io_loop.run_until_complete(
            super().update_many(upsert, session, **query)
        )

    @no_type_check
    def update_one(
        self, upsert: bool = False, session: Optional[ClientSession] = None, **query
    ) -> int:
        return self._io_loop.run_until_complete(
            super().update_one(upsert, session, **query)
        )

    @no_type_check
    def count(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        return self._io_loop.run_until_complete(
            super().count(logical_query, session, **query)
        )

    @no_type_check
    def count_documents(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        **query,
    ) -> int:
        return self._io_loop.run_until_complete(
            super().count_documents(logical_query, session, **query)
        )

    @no_type_check
    def distinct(
        self, field: str, session: Optional[ClientSession] = None, **query
    ) -> list:
        return self._io_loop.run_until_complete(
            super().distinct(field, session, **query)
        )

    @no_type_check
    def raw_aggregate(
        self, data: List[Dict[Any, Any]], session: Optional[ClientSession] = None
    ) -> list:
        return self._io_loop.run_until_complete(super().raw_aggregate(data, session))

    @no_type_check
    def raw_query(
        self,
        method_name: str,
        raw_query: Union[Dict, List[Dict], Tuple[Dict]],
        session: Optional[ClientSession] = None,
    ) -> Any:
        return self._io_loop.run_until_complete(
            super().raw_query(method_name, raw_query, session)
        )

    @no_type_check
    def replace_one(
        self,
        replacement: Dict,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **filter_query,
    ) -> Any:
        return self._io_loop.run_until_complete(
            super().replace_one(replacement, upsert, session, **filter_query)
        )

    @no_type_check
    def find_with_count(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        skip_rows: Optional[int] = None,
        limit_rows: Optional[int] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        **query,
    ) -> Tuple[int, FindResult]:
        return self._io_loop.run_until_complete(
            super().find_with_count(
                logical_query,
                skip_rows,
                limit_rows,
                session,
                sort_fields,
                sort,
                **query,
            )
        )

    @no_type_check
    def simple_aggregate(self, *args, **kwargs) -> SimpleAggregateResult:
        return self._io_loop.run_until_complete(
            super().simple_aggregate(*args, **kwargs)
        )

    @no_type_check
    def aggregate_sum(self, agg_field: str, **query) -> Union[int, float]:
        return self._io_loop.run_until_complete(
            super().aggregate_sum(agg_field, **query)
        )

    @no_type_check
    def aggregate_min(self, agg_field: str, **query) -> Union[int, float]:
        return self._io_loop.run_until_complete(
            super().aggregate_min(agg_field, **query)
        )

    @no_type_check
    def aggregate_max(self, agg_field: str, **query) -> Union[int, float]:
        return self._io_loop.run_until_complete(
            super().aggregate_max(agg_field, **query)
        )

    @no_type_check
    def aggregate_avg(self, agg_field: str, **query) -> Union[int, float]:
        return self._io_loop.run_until_complete(
            super().aggregate_avg(agg_field, **query)
        )

    @no_type_check
    def drop_collection(self, force: bool = False) -> bool:
        return self._io_loop.run_until_complete(super().drop_collection(force))

    @no_type_check
    def find_and_replace(
        self,
        replacement: Union[dict, Any],
        projection_fields: Optional[list] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **query,
    ) -> Union[Dict, 'MongoModel', None]:
        return self._io_loop.run_until_complete(
            super().find_and_replace(
                replacement,
                projection_fields,
                sort_fields,
                sort,
                upsert,
                session,
                **query,
            )
        )

    @no_type_check
    def find_one_and_update(
        self,
        projection_fields: Optional[list] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        upsert: bool = False,
        session: Optional[ClientSession] = None,
        **query,
    ) -> Union[Dict, 'MongoModel', None]:
        return self._io_loop.run_until_complete(
            super().find_one_and_update(
                projection_fields, sort_fields, sort, upsert, session, **query
            )
        )

    @no_type_check
    def bulk_update_or_create(
        self,
        models: List,
        query_fields: List,
        batch_size: Optional[int] = 10000,
        session: Optional[ClientSession] = None,
    ) -> None:
        return self._io_loop.run_until_complete(
            super().bulk_update_or_create(models, query_fields, batch_size, session)
        )

    @no_type_check
    def bulk_create(
        self,
        models: List,
        batch_size: Optional[int] = 30000,
        session: Optional[ClientSession] = None,
    ) -> int:
        return self._io_loop.run_until_complete(
            super().bulk_create(models, batch_size, session)
        )

    @no_type_check
    def get_or_create(self, **query) -> Tuple:
        """like django orm get_or_create

        Returns:
            Tuple: MongoModel instance, True/False
        """
        defaults = query.pop('defaults', {})
        with_relations_objects = query.pop('with_relations_objects', False)
        obj = self.find_one(**query, with_relations_objects=with_relations_objects)
        if obj:
            created = False
        else:
            created = True
            inserted_id = self.insert_one(**{**query, **defaults})
            obj = self.find_one(
                _id=inserted_id, with_relations_objects=with_relations_objects
            )
        return obj, created

    @no_type_check
    def update_or_create(self, **query) -> Tuple:
        """like django orm update_or_create

        Returns:
            Tuple: MongoModel instance, True/False
        """
        defaults = query.pop('defaults', {})
        with_relations_objects = query.pop('with_relations_objects', False)
        obj = self.find_one(**query, with_relations_objects=with_relations_objects)
        if obj is not None:
            created = False
            for field, value in defaults.items():
                setattr(obj, field, value)
        else:
            created = True
            obj = self.mongo_model_class(**{**query, **defaults})  # type: ignore
        obj.save_sync()
        if with_relations_objects:
            obj = self.get(_id=obj._id, with_relations_objects=with_relations_objects)
        return obj, created

    @no_type_check
    def get(
        self,
        logical_query: Union[Query, QueryCombination, None] = None,
        session: Optional[ClientSession] = None,
        sort_fields: Optional[Union[Tuple, List]] = None,
        sort: Optional[int] = None,
        with_relations_objects: bool = False,
        **query,
    ) -> Any:
        """method like django orm get

        Args:
            logical_query (Union[Query, QueryCombination, None], optional): Query objects. Defaults to None.
            session (Optional[ClientSession], optional): mongo session. Defaults to None.
            sort_fields (Optional[Union[Tuple, List]], optional): sorts. Defaults to None.
            sort (Optional[int], optional): sort. Defaults to None.

        Raises:
            DoesNotExist: raise if not found object

        Returns:
            Any: mongo model
        """

        obj = self.find_one(
            logical_query=logical_query,
            session=session,
            sort_fields=sort_fields,
            sort=sort,
            **query,
        )
        if not obj:
            raise DoesNotExist(self.mongo_model_class.__name__)  # type: ignore
        if with_relations_objects and self.mongo_model_class.relation_manager:
            obj = self._io_loop.run_until_complete(
                self.mongo_model_class.relation_manager.map_relation_for_single(obj)
            )
        return obj
