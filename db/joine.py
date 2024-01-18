import sqlalchemy as sa
import typing as t

from datetime import date, time, datetime, timedelta

from init import TZ
from .base import begin_connection
from .sessions import SessionTable
from .tasks import TaskTable


class LastTaskRow (t.Protocol):
    session_id: int
    task_id: int
    user_id: int
    date: date
    time: time
    duration: int
    name: str


class ReportDailyRow (t.Protocol):
    date: date
    duration: int
    name: str


class ReportGlobalRow (t.Protocol):
    duration: int
    name: str


# возвращает текущую задачу
async def get_last_task() -> LastTaskRow:
    query = (
        sa.select (
            SessionTable.c.id.label('session_id'),
            SessionTable.c.task_id,
            TaskTable.c.user_id,
            SessionTable.c.date,
            SessionTable.c.time,
            SessionTable.c.duration,
            TaskTable.c.name
        )
        .select_from (SessionTable.join (TaskTable, SessionTable.c.task_id == TaskTable.c.id))
    ).order_by (sa.desc (SessionTable.c.id)).limit (1)
    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.first ()


# дневной отчёт
async def get_daily_report(task_id: int = 0) -> tuple[ReportDailyRow]:
    today = datetime.now(TZ).date()
    query = (
        sa.select (
            SessionTable.c.date,
            TaskTable.c.name,
            sa.func.sum (SessionTable.c.duration).label ('duration')
        )
        .select_from (SessionTable.join (TaskTable, SessionTable.c.task_id == TaskTable.c.id))
        .group_by (SessionTable.c.date, TaskTable.c.name)
        .where (SessionTable.c.in_google == False)
        # .where (SessionTable.c.date == today)
    )

    if task_id != 0:
        query = query.where(SessionTable.c.task_id == task_id)

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()


# дневной отчёт
async def get_global_report(task_id: int = 0) -> tuple[ReportGlobalRow]:
    query = (sa.select(
        TaskTable.c.create_at,
        TaskTable.c.name,
        sa.func.sum(SessionTable.c.duration).label('duration')
    ).select_from(SessionTable.join (TaskTable, SessionTable.c.task_id == TaskTable.c.id)).
             group_by(TaskTable.c.create_at, TaskTable.c.name)).order_by(sa.desc(TaskTable.c.create_at))

    if task_id != 0:
        query = query.where(SessionTable.c.task_id == task_id)

    async with begin_connection () as conn:
        result = await conn.execute (query)

    return result.all ()