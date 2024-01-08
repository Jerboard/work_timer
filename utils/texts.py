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

        work_min = round(time_work.total_seconds() / 60)

        if task_info[0].duration:
            today_duration = task_info[0].duration + work_min
        else:
            today_duration = work_min

        if global_info [0].duration:
            global_duration = global_info [0].duration + today_duration

        else:
            global_duration = today_duration

        text = (
            f'<b>Работаешь над:</b> {last_task.name}\n'
            f'<b>Всего:</b> {process_duration(global_duration)}\n'
            f'<b>Сегодня:</b> {process_duration(today_duration)}\n'
            f'<b>Уже:</b> {process_duration(work_min)}'
        )
    else:
        text = f'<b>Нет текущих задач</b>'

    return text