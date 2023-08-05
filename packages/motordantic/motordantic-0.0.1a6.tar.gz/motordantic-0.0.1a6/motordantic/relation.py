import asyncio
from typing import TYPE_CHECKING, List

from .types import RelationTypes

__all__ = ('RelationManager',)

if TYPE_CHECKING:
    from .models import MongoModel
    from .typing import DictStrList, MONGO_MODEL_TYPE


class RelationManager(object):
    """relation manager for get and set data from to to models instances"""

    __slots__ = ('mongo_model_class', 'relation_fields')

    def __init__(self, mongo_model_class: 'MONGO_MODEL_TYPE'):
        self.mongo_model_class = mongo_model_class
        self.relation_fields = self._get_relation_fields(mongo_model_class)

    @classmethod
    def _get_relation_fields(cls, mongo_model_class: 'MONGO_MODEL_TYPE') -> dict:
        return mongo_model_class.__db_refs__ or {}

    def _relation_data_setter(
        self, mongo_model: 'MongoModel', data: dict
    ) -> 'MongoModel':
        """data setter

        Args:
            mongo_model (MongoModel): mongo model insatance
            data (dict): relations objects map

        Returns:
            MongoModel: updated mongo model
        """
        for field, relation_info in self.relation_fields.items():
            relation_attr = getattr(mongo_model, field)
            if not relation_attr:
                continue
            if relation_info.relation_type == RelationTypes.ARRAY:
                relation_value = []
                for rel in relation_attr:
                    v = data[field].get(str(rel.db_ref.id))
                    if v:
                        relation_value.append(v)
            else:
                relation_value = data[field].get(str(relation_attr.db_ref.id))
            setattr(mongo_model, field, relation_value)
        return mongo_model

    async def get_relation_objects(self, pre_relation: 'DictStrList') -> dict:
        futures = []
        field_map = {}
        for index_, row in enumerate(pre_relation.items(), start=1):
            field, ids = row
            mongo_model_class = self.relation_fields[field].mongo_model_class
            futures.append(
                asyncio.ensure_future(
                    mongo_model_class.Q.find(_id__in=ids, with_relations_objects=True)
                )
            )
            field_map[index_] = field

        relation_objects = {}
        for index_, field_relation_result in enumerate(
            asyncio.as_completed(futures), start=1
        ):
            field = field_map[index_]
            relation_objects[field] = {
                str(o._id): o for o in await field_relation_result
            }
        return relation_objects

    def _get_pre_relation(
        self, mongo_model_instances: List['MongoModel']
    ) -> 'DictStrList':
        pre_relation: 'DictStrList' = {field: [] for field in self.relation_fields}
        for mongo_model_instance in mongo_model_instances:
            for field in self.relation_fields:
                attr = getattr(mongo_model_instance, field)
                if isinstance(attr, list):
                    ids = tuple(row.db_ref.id for row in attr)
                else:
                    ids = (attr.db_ref.id,) if attr else tuple()
                if ids:
                    pre_relation[field].extend(ids)
        return {f: list(set(items)) for f, items in pre_relation.items()}

    async def map_relation_for_single(
        self, mongo_model_instance: 'MongoModel'
    ) -> 'MongoModel':
        """map relation data to mongo model instanc

        Args:
            mongo_model_instances (List[MongoModel]): list of instances from MongoModel

        Returns:
            MongoModel: mapped mongo model
        """
        pre_relation: 'DictStrList' = self._get_pre_relation([mongo_model_instance])
        relation_objects = await self.get_relation_objects(pre_relation)
        return self._relation_data_setter(mongo_model_instance, relation_objects)

    async def map_relation_for_array(self, result: List) -> List['MongoModel']:
        """map relations data for _find method list result

        Args:
            result (List): _find query result converted to list

        Returns:
            List: mapped list
        """
        pre_relation: 'DictStrList' = self._get_pre_relation(result)
        relation_objects = await self.get_relation_objects(pre_relation)
        generated_result = [
            self._relation_data_setter(r, relation_objects) for r in result
        ]
        return generated_result
