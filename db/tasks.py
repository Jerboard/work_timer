import sqlalchemy as sa
import typing as t
from sqlalchemy.exc import OperationalError
from datetime import datetime, date, timedelta, time

from init import TZ, log_error
from db.base import METADATA, begin_connection


class TaskRow(t.Protocol):
    id: int
    user_id: int
    create_at: datetime
    name: str
    status: str


TaskTable = sa.Table(
    'tasks',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger()),
    sa.Column('create_at', sa.DateTime()),
    sa.Column('name', sa.String(255)),
    sa.Column('status', sa.String(255)),
)


# возвращает текущую задачу
async def get_all_task() -> tuple[TaskRow]:
    async with begin_connection() as conn:
        result = await conn.execute(
            TaskTable.select().where(TaskTable.c.status == 'active')
        )
    return result.all()


# добавить задачу
async def add_task(user_id: int, name: str) -> bool:
    try:
        async with begin_connection() as conn:
            await conn.execute(
                TaskTable.insert().values(
                    user_id=user_id,
                    create_at=datetime.now(TZ),
                    name=name,
                    status='active'
                )
            )
        return True
    except OperationalError as ex:
        log_error(ex)
        return False


# изменить задачу
async def update_task(task_id: int, name: str = None, status: str = None) -> None:
    query = TaskTable.update().where(TaskTable.c.id == task_id)
    if name:
        query = query.values(name=name)
    if status:
        query = query.values (status=status)

    async with begin_connection() as conn:
        await conn.execute(query)
