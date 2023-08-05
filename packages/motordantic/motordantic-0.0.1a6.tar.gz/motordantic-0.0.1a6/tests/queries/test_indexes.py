import pytest
import pytest_asyncio
from pymongo import IndexModel

from motordantic.models import MongoModel
from motordantic.exceptions import MotordanticIndexError


class IndexTicket(MongoModel):
    name: str
    position: int
    config: dict

    class Config:
        indexes = [
            IndexModel([('position', 1)]),
            IndexModel([('name', 1)]),
        ]


@pytest_asyncio.fixture(scope='session', autouse=True)
async def drop_ticket_collection(event_loop):
    await IndexTicket.ensure_indexes()
    yield
    await IndexTicket.Q.drop_collection(force=True)


@pytest.mark.asyncio
async def test_check_indexes():
    result = await IndexTicket.Q.list_indexes()
    assert result == {
        '_id_': {'key': {'_id': 1}},
        'position_1': {'key': {'position': 1}},
        'name_1': {'key': {'name': 1}},
    }


@pytest.mark.asyncio
async def test_check_indexes_if_remove():
    class IndexTicket(MongoModel):
        name: str
        position: int
        config: dict

        class Config:
            indexes = [
                IndexModel([('position', 1)]),
            ]

    await IndexTicket.ensure_indexes()
    result = await IndexTicket.Q.list_indexes()
    assert result == {
        '_id_': {'key': {'_id': 1}},
        'position_1': {'key': {'position': 1}},
    }


@pytest.mark.asyncio
async def test_drop_index():
    with pytest.raises(MotordanticIndexError):
        result = await IndexTicket.Q.drop_index('position1111')

    result = await IndexTicket.Q.drop_index('position_1')
    assert result == 'position_1 dropped.'
