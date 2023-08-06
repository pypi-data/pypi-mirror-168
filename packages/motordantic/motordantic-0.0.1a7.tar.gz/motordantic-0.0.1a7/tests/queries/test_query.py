import pytest
import pytest_asyncio

from motordantic.models import MongoModel
from motordantic.query import Query


class TicketForQuery(MongoModel):
    name: str
    position: int


@pytest_asyncio.fixture(scope='session', autouse=True)
async def drop_ticket_collection(event_loop):
    yield
    await TicketForQuery.Q.drop_collection(force=True)


def test_query_organization():
    query = (
        Query(name=123) | Query(name__ne=124) & Query(position=1) | Query(position=2)
    )
    data = query.to_query(TicketForQuery)
    value = {
        '$or': [
            {'name': '123'},
            {'$and': [{'name': {'$ne': '124'}}, {'position': 1}]},
            {'position': 2},
        ]
    }
    assert data == value


@pytest.mark.asyncio
async def test_query_result():
    query = [
        TicketForQuery(name='first', position=1),
        TicketForQuery(name='second', position=2),
    ]
    inserted = await TicketForQuery.Q.insert_many(query)
    assert inserted == 2

    query = Query(name='first') | Query(position=1) & Query(name='second')
    data = await TicketForQuery.Q.find_one(query)
    assert data.name == 'first'

    query = Query(position=3) | Query(position=1) & Query(name='second')
    data = await TicketForQuery.Q.find_one(query)
    assert data is None

    query = Query(position=3) | Query(position=2) & Query(name='second')
    data = await TicketForQuery.Q.find_one(query)
    assert data.name == 'second'
