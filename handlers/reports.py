from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


import json
from datetime import datetime

import db
from init import dp, TZ, bot, DATE_STR_FORMAT
from keyboards import inline_kb as kb
from utils.func import process_duration
from utils.google_api import send_daily_report_in_table, send_global_report_in_table


# начинает задачу
@dp.callback_query(lambda cb: cb.data.startswith('report_daily'))
async def new_task(cb: CallbackQuery, state: FSMContext):
    sent  = await cb.message.answer('⏳')
    daily_report = await db.get_daily_report()

    in_table_daily = []
    for task in daily_report:
        in_table_daily.append(
            [task.date.strftime(DATE_STR_FORMAT), task.name, process_duration(task.duration)]
        )

    await send_daily_report_in_table(in_table_daily)

    global_report = await db.get_global_report ()

    in_table_global = []
    for task in global_report:
        in_table_global.append (
            [task.name, process_duration (task.duration)]
        )

    await send_global_report_in_table(in_table_global)
    await sent.delete()

