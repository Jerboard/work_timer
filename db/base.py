import typing as t
import sqlalchemy as sa
import logging

from sqlalchemy.ext.asyncio import AsyncConnection

from init import ENGINE

METADATA = sa.MetaData()


def begin_connection() -> t.AsyncContextManager[AsyncConnection]:
    pool = ENGINE.pool
    active_connections = pool.checkedout ()
    available_connections = pool.checkedin ()
    logging.warning (f"Количество активных соединений: {active_connections}")
    logging.warning (f"Количество соединений в пуле: {available_connections}")

    ENGINE.connect ()
    return ENGINE.begin ()


async def init_models():
    async with ENGINE.begin() as conn:
        await conn.run_sync(METADATA.create_all)