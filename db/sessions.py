import sqlalchemy as sa
import typing as t
import logging

from datetime import datetime, date, timedelta, time

from init import TZ, log_error
from db.base import METADATA, begin_connection


class SessionRow(t.Protocol):
    id: int
    task_id: int
    date: date
    time: time
    duration: int


SessionTable = sa.Table(
    'sessions',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('task_id', sa.Integer()),
    sa.Column('date', sa.Date()),
    sa.Column('time', sa.Time()),
    sa.Column('duration', sa.Integer()),
)


# закрывает текущую задачу
async def close_last_task(time_start: datetime, session_id: int):
    now = datetime.now (TZ)
    time_work = now - TZ.localize(time_start)
    minutes = round (time_work.total_seconds () / 60)

    async with begin_connection() as conn:
        await conn.execute(
            SessionTable.update().values(duration=minutes).where(SessionTable.c.id == session_id))


# начинает новую рабочую сессию задачу
async def start_new_session(task_id: int):
    now = datetime.now (TZ)
    async with begin_connection() as conn:
        await conn.execute(
            SessionTable.insert().values(
                task_id=task_id,
                date=now.date(),
                time=now.time(),
            ))
