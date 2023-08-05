from typing import Type, TYPE_CHECKING, List, Dict, Any, Union, AbstractSet, Set

if TYPE_CHECKING:
    from .models import MongoModel

__all__ = (
    'MONGO_MODEL_TYPE',
    'DictStrList',
    'DictStrAny',
    'DictAny',
    'SetStr',
    'ListStr',
    'IntStr',
    'AbstractSetIntStr',
    'DictIntStrAny',
)

MONGO_MODEL_TYPE = Type['MongoModel']
DictStrList = Dict[str, List]
DictStrAny = Dict[str, Any]
DictAny = Dict[Any, Any]
SetStr = Set[str]
ListStr = List[str]
IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
DictIntStrAny = Dict[IntStr, Any]
