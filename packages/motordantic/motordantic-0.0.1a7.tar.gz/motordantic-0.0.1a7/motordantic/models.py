import json
from typing import (
    Dict,
    Any,
    Union,
    Optional,
    List,
    Tuple,
    TYPE_CHECKING,
    ClassVar,
)

from bson import ObjectId, DBRef
from motor.core import AgnosticClientSession, AgnosticCollection, AgnosticDatabase

from pydantic.main import ModelMetaclass as PydanticModelMetaclass
from pydantic import BaseModel as BasePydanticModel, root_validator
from pymongo import IndexModel


from .relation import RelationManager
from .types import ObjectIdStr, RelationInfo, Relation
from .exceptions import (
    NotDeclaredField,
    MotordanticInvalidArgsParams,
    MotordanticValidationError,
    MotordanticConnectionError,
)
from .property import classproperty
from .validaton import validate_field_value
from .extra import ExtraQueryMapper, take_relation
from .query import Query, QueryCombination
from .querybuilder import QueryBuilder

__all__ = ('MongoModel', 'ModelMetaclass')

if TYPE_CHECKING:
    from .typing import DictStrAny, AbstractSetIntStr, SetStr, MONGO_MODEL_TYPE


_is_mongo_model_class_defined = False


class ModelMetaclass(PydanticModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):  # type: ignore
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        indexes = set()
        if _is_mongo_model_class_defined and issubclass(cls, MongoModel):
            querybuilder = getattr(cls, '__querybuilder__')
            if querybuilder is None:
                querybuilder = QueryBuilder(cls)  # type: ignore
                setattr(cls, '__querybuilder__', querybuilder)
            db_refs = {}
            for k, v in cls.__fields__.items():
                relation_info = take_relation(v)
                if relation_info is not None:
                    db_refs[k] = relation_info
            setattr(cls, '__db_refs__', db_refs)
            if db_refs:
                setattr(cls, '__relation_manager__', RelationManager(cls))
        json_encoders = getattr(cls.Config, 'json_encoders', {})  # type: ignore
        json_encoders.update({ObjectId: lambda f: str(f)})
        setattr(cls.Config, 'json_encoders', json_encoders)  # type: ignore
        exclude_fields = getattr(cls.Config, 'exclude_fields', tuple())  # type: ignore
        setattr(cls, '__indexes__', indexes)
        setattr(cls, '__database_exclude_fields__', exclude_fields)
        return cls


class MongoModel(BasePydanticModel, metaclass=ModelMetaclass):
    __database__: Optional[AgnosticDatabase] = None
    __collection__: Optional[AgnosticCollection] = None
    __indexes__: 'SetStr' = set()
    __database_exclude_fields__: Union[Tuple, List] = tuple()
    __querybuilder__: Optional[QueryBuilder] = None
    __db_refs__: ClassVar[Optional[Dict[str, RelationInfo]]] = None
    __relation_manager__: Optional[RelationManager] = None
    _id: Optional[ObjectIdStr] = None

    def __setattr__(self, key, value):
        if key == '_id':
            self.__dict__[key] = value
            return value
        else:
            return super().__setattr__(key, value)

    @classproperty
    def relation_manager(cls) -> Optional[RelationManager]:
        return cls.__relation_manager__

    @classmethod
    async def _start_session(cls) -> AgnosticClientSession:
        return await cls.Q.motor_client.start_session()

    @classmethod
    async def ensure_indexes(cls):
        """method for create/update/delete indexes if indexes declared in Config property"""

        indexes = getattr(cls.__config__, 'indexes', [])
        if not all([isinstance(index, IndexModel) for index in indexes]):
            raise ValueError('indexes must be list of IndexModel instances')
        if indexes:
            db_indexes = await cls.Q.list_indexes()
            indexes_to_create = [
                i for i in indexes if i.document['name'] not in db_indexes
            ]
            indexes_to_delete = [
                i
                for i in db_indexes
                if i not in [i.document['name'] for i in indexes] and i != '_id_'
            ]
            result = []
            if indexes_to_create:
                try:
                    result = await cls.Q.create_indexes(indexes_to_create)
                except MotordanticConnectionError:
                    pass
            if indexes_to_delete:
                for index_name in indexes_to_delete:
                    await cls.Q.drop_index(index_name)
                db_indexes = await cls.Q.list_indexes()
            indexes = set(list(db_indexes.keys()) + result)
        setattr(cls, '__indexes__', indexes)

    @classmethod
    def _get_properties(cls) -> list:
        return [
            prop
            for prop in dir(cls)
            if prop
            not in (
                "__values__",
                "fields",
                "data",
                "_connection",
                "_collection_name",
                "_collection",
                "querybuilder",
                "Q",
                "AQ",
                "pk",
                "_query_data",
                "fields_all",
                "all_fields",
            )
            and isinstance(getattr(cls, prop), property)
        ]

    @classmethod
    def parse_obj(cls, data: Any) -> Any:
        obj = super().parse_obj(data)
        if '_id' in data:
            obj._id = data['_id'].__str__()
        return obj

    async def save(
        self,
        updated_fields: Union[Tuple, List] = [],
        session: Optional[AgnosticClientSession] = None,
    ) -> Any:
        if self._id is not None:
            data = {
                '_id': (
                    self._id if isinstance(self._id, ObjectId) else ObjectId(self._id)
                )
            }
            if updated_fields:
                if not all(field in self.__fields__ for field in updated_fields):
                    raise MotordanticValidationError('invalid field in updated_fields')
            else:
                updated_fields = tuple(self.__fields__.keys())
            for field in updated_fields:
                data[f'{field}__set'] = getattr(self, field)
            await self.Q.update_one(
                session=session,
                **data,
            )
            return self
        data = {
            field: value
            for field, value in self.__dict__.items()
            if field in self.__fields__
        }
        object_id = await self.Q.insert_one(
            session=session,
            **data,
        )
        self._id = object_id
        return self

    def save_sync(
        self,
        updated_fields: Union[Tuple, List] = [],
        session: Optional[AgnosticClientSession] = None,
    ):
        return self.Q.sync._io_loop.run_until_complete(
            self.save(updated_fields, session)
        )

    async def delete(self) -> None:
        await self.Q.delete_one(_id=self.pk)

    def delete_sync(self) -> None:
        return self.Q.sync._io_loop.run_until_complete(self.delete())

    @classmethod
    def __validate_field(cls, field: str) -> bool:
        if field not in cls.__fields__ and field != '_id':
            raise NotDeclaredField(field, list(cls.__fields__.keys()))
        elif field in cls.__database_exclude_fields__:
            return False
        return True

    @classmethod
    def _check_query_args(
        cls,
        logical_query: Union[
            List[Any], Dict[Any, Any], str, Query, QueryCombination, None
        ] = None,
    ) -> 'DictStrAny':
        """check if query = Query obj or QueryCombination

        Args:
            logical_query (Union[ List[Any], Dict[Any, Any], str, Query, QueryCombination ], optional): Query | QueryCombination. Defaults to None.

        Raises:
            InvalidArgsParams: if not Query | QueryCombination

        Returns:
            Dict: generated query dict
        """
        if not isinstance(logical_query, (QueryCombination, Query)):
            raise MotordanticInvalidArgsParams()
        return logical_query.to_query(cls)  # type: ignore

    @classmethod
    def use(cls: 'MONGO_MODEL_TYPE', database: AgnosticDatabase) -> None:
        assert database is not None
        cls.__database__ = database

    @classmethod
    def _parse_extra_params(cls, extra_params: List) -> tuple:
        field_param, extra = [], []
        methods = ExtraQueryMapper.methods
        for param in extra_params:
            if param in methods:
                extra.append(param)
            else:
                field_param.append(param)
        return field_param, extra

    @classmethod
    def _validate_query_data(cls, query: Dict) -> 'DictStrAny':
        """main validation method

        Args:
            query (Dict): basic query

        Returns:
            Dict: parsed query
        """
        data: dict = {}
        for query_field, value in query.items():
            field, *extra_params = query_field.split("__")
            inners, extra_params = cls._parse_extra_params(extra_params)
            if not cls.__validate_field(field):
                continue
            extra = ExtraQueryMapper(cls, field).query(extra_params, value)
            if extra:
                value = extra[field]
            elif field == '_id':
                value = ObjectId(value)
            else:
                value = validate_field_value(cls, field, value) if not inners else value
            if inners:
                field = f'{field}.{".".join(i for i in inners)}'
            if (
                extra
                and field in data
                and ('__gt' in query_field or '__lt' in query_field)
            ):
                data[field].update(value)
            else:
                data[field] = value
        return data

    @classproperty
    def database(cls) -> AgnosticDatabase:
        """Returns the database that is currently associated with this document."""
        if not hasattr(cls, "__database__") or cls.__database__ is None:
            raise AttributeError("Accessing database without using it first.")
        return cls.__database__

    @classproperty
    def collection(cls: 'MongoModel') -> AgnosticCollection:
        """Returns the collection for this :class:`MongoModel`."""
        if (
            cls.__collection__ is None
            or cls.__collection__.database is not cls.database
        ):
            cls.__collection__ = cls.database.get_collection(cls.set_collection_name())  # type: ignore
        return cls.__collection__

    @classproperty
    def fields_all(cls) -> list:
        """return all fields with properties(not document fields)"""
        fields = list(cls.__fields__.keys())
        return_fields = fields + cls._get_properties()
        return return_fields

    @classproperty
    def Q(cls) -> Optional[QueryBuilder]:
        return cls.__querybuilder__

    def dict(  # type: ignore
        self,
        *,
        include: Optional['AbstractSetIntStr'] = None,
        exclude: Optional['AbstractSetIntStr'] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        with_props: bool = True,
    ) -> 'DictStrAny':
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        attribs = super().dict(
            include=include,  # type: ignore
            exclude=exclude,  # type: ignore
            by_alias=by_alias,
            skip_defaults=skip_defaults,  # type: ignore
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if with_props:
            props = self._get_properties()
            # Include and exclude properties
            if include:
                props = [prop for prop in props if prop in include]
            if exclude:
                props = [prop for prop in props if prop not in exclude]

            # Update the attribute dict with the properties
            if props:
                attribs.update({prop: getattr(self, prop) for prop in props})
        if self.has_db_refs():
            for field in self.__db_refs__:  # type: ignore
                attrib_data = attribs[field]
                if attrib_data and not isinstance(attrib_data, dict):
                    attribs[field] = (
                        attrib_data.to_dict()
                        if not isinstance(attrib_data, list)
                        else [
                            a.to_dict() if not isinstance(a, dict) else a
                            for a in attrib_data
                        ]
                    )
        return attribs

    @classmethod
    def to_relation(cls, object_id: Union[str, ObjectId]) -> Relation:
        if isinstance(object_id, str):
            object_id = ObjectId(object_id)
        db_ref = DBRef(collection=cls.set_collection_name(), id=object_id)
        return Relation(db_ref, cls)

    @classmethod
    def has_db_refs(cls) -> bool:
        return bool(cls.__db_refs__)

    @property
    def data(self) -> 'DictStrAny':
        return self.dict(with_props=True)

    @property
    def _query_data(self) -> 'DictStrAny':
        return self.dict(with_props=False)

    @classmethod
    def set_collection_name(cls) -> str:
        """main method for set collection

        Returns:
            str: collection name
        """
        return cls.__name__.lower()

    def serialize(self, fields: Union[Tuple, List]) -> 'DictStrAny':
        data: dict = self.dict(include=set(fields))
        return {f: data[f] for f in fields}

    def serialize_json(self, fields: Union[Tuple, List]) -> str:
        return json.dumps(self.serialize(fields))

    @property
    def pk(self):
        return self._id

    @root_validator
    def validate_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, MongoModel):
                raise ValueError(
                    f'{field} - cant be instance of MongoModel without Relation'
                )
        return values


_is_mongo_model_class_defined = True
