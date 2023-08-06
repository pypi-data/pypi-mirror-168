from typing import Optional, TypeVar, Generic, Union, TYPE_CHECKING
from enum import Enum

from bson import ObjectId, DBRef
from bson.errors import InvalidId
from pydantic import parse_obj_as, BaseModel
from pydantic.fields import ModelField
from pydantic.json import ENCODERS_BY_TYPE

from .typing import MONGO_MODEL_TYPE

__all__ = ('ObjectIdStr', 'Relation', 'RelationInfo', 'RelationTypes')

if TYPE_CHECKING:
    from .models import MongoModel

T = TypeVar("T")


class ObjectIdStr(str):
    """Field for validate string like ObjectId"""

    type_ = ObjectId
    required = False
    default = None
    validate_always = False
    alias = ''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError(f"invalid ObjectId - {v}")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class RelationTypes(str, Enum):
    SINGLE = "SINGLE"
    OPTIONAL_SINGLE = "OPTIONAL_SINGLE"
    ARRAY = "ARRAY"


class RelationInfo(BaseModel):
    field: str
    mongo_model_class: MONGO_MODEL_TYPE
    relation_type: RelationTypes


class Relation(Generic[T]):
    def __init__(self, db_ref: DBRef, mongo_model_class: MONGO_MODEL_TYPE):
        self.db_ref = db_ref
        self.mongo_model_class = mongo_model_class

    async def get(self) -> Optional["MongoModel"]:
        result = await self.mongo_model_class.Q.find_one(_id=self.db_ref.id, with_relations_objects=True)  # type: ignore
        return result

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def _validate_for_model(
        cls, v: Union[dict, BaseModel], mongo_model_class: MONGO_MODEL_TYPE
    ) -> 'Relation':
        parsed = (
            mongo_model_class.parse_obj(v)
            if isinstance(v, dict)
            else mongo_model_class.validate(v)
        )
        new_id = (
            parsed._id
            if isinstance(parsed._id, ObjectId)
            else parse_obj_as(
                ObjectIdStr,
                parsed._id,  # type: ignore
            )
        )
        db_ref = DBRef(collection=mongo_model_class.set_collection_name(), id=new_id)
        return cls(db_ref=db_ref, mongo_model_class=mongo_model_class)

    @classmethod
    def validate(cls, v: Union[DBRef, T], field: ModelField):
        mongo_model_class = field.sub_fields[0].type_  # type: ignore
        if isinstance(v, DBRef):
            return cls(db_ref=v, mongo_model_class=mongo_model_class)
        if isinstance(v, Relation):
            return v
        if isinstance(v, dict):
            try:
                return cls(db_ref=DBRef(**v), mongo_model_class=mongo_model_class)
            except TypeError:
                return cls._validate_for_model(v, mongo_model_class)
        if isinstance(v, BaseModel):
            return cls._validate_for_model(v, mongo_model_class)
        raise ValueError(f'invalod type - {v}')

    def to_ref(self):
        return self.db_ref

    def to_dict(self):
        return {"id": str(self.db_ref.id), "collection": self.db_ref.collection}

    @property
    def data(self):
        return self.to_dict()


ENCODERS_BY_TYPE[Relation] = lambda o: o.to_dict()
ENCODERS_BY_TYPE[ObjectIdStr] = lambda o: str(o)
