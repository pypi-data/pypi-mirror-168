from contextlib import ContextDecorator

from .typing import MONGO_MODEL_TYPE


class Session(ContextDecorator):
    __slots__ = (
        '_session',
        'mongo_model_class',
    )

    def __init__(self, mongo_model_class: MONGO_MODEL_TYPE):
        self.mongo_model_class = mongo_model_class

    async def __aenter__(self):
        self._session = await self.mongo_model_class._start_session()
        return self._session

    async def __aexit__(self, *args, **kwargs):
        await self._session.end_session()  # type: ignore

    async def start_stransaction(
        self,
        read_concern=None,
        write_concern=None,
        read_preference=None,
        max_commit_time_ms=None,
    ):
        # TODO tranaction login with rs
        return self._session.start_transaction(
            read_preference=read_preference,
            write_concern=write_concern,
            read_concern=read_concern,
            max_commit_time_ms=max_commit_time_ms,
        )


class SessionSync(ContextDecorator):
    __slots__ = (
        '_session',
        'mongo_model_class',
    )

    def __init__(self, mongo_model_class: MONGO_MODEL_TYPE):
        self.mongo_model_class = mongo_model_class

    def __enter__(self):
        self._session = self.mongo_model_class.Q.sync._io_loop.run_until_complete(
            self.mongo_model_class._start_session()
        )
        return self._session

    def __exit__(self, *args, **kwargs):
        return self.mongo_model_class.Q.sync._io_loop.run_until_complete(self._session.end_session())  # type: ignore)
