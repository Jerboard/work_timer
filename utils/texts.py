from datetime import datetime

import db

from init import TZ
from utils.func import process_duration


async def get_start_text() -> str:
    last_task = await db.get_last_task()
    task_info = await db.get_daily_report(task_id=last_task.task_id)
    global_info = await db.get_global_report(task_id=last_task.task_id)

    if last_task and last_task.duration is None:
        now = datetime.now (TZ)
        last_task_start = datetime.combine (last_task.date, last_task.time)
        time_work = now - TZ.localize(last_task_start)
        time_work_str = process_duration(round(time_work.total_seconds() / 60))
        text = (
            f'<b>Работаешь над:</b> {last_task.name}\n'
            f'<b>Всего:</b> {global_info[0].duration}\n'
            f'<b>Сегодня:</b> {task_info[0].duration}\n'
            f'<b>Уже:</b> {time_work_str}'
        )
    else:
        text = f'<b>Нет текущих задач</b>'

    return text