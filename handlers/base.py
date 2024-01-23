from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


import json
from datetime import datetime

import db
from init import dp, TZ, bot
from keyboards import inline_kb as kb
from utils.texts import get_start_text
from utils.filters import alien_message


# команда старт
@dp.message(lambda msg: alien_message(msg.from_user.id))
async def alien_filter(msg: Message, state: FSMContext):
    pass


# команда старт
@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    await state.clear()
    text = await get_start_text()
    tasks = await db.get_all_task()

    await msg.answer(text, reply_markup=kb.get_start_kb(tasks))


# возвращает стартовый экран
@dp.callback_query(lambda cb: cb.data.startswith('back_start'))
async def edit_task(cb: CallbackQuery, state: FSMContext):
    await state.clear ()
    text = await get_start_text ()
    tasks = await db.get_all_task ()
    try:
        await cb.message.edit_text (text, reply_markup=kb.get_start_kb (tasks))
    except TelegramBadRequest as ex:
        await cb.answer('Нечего обновлять')


# начинает задачу
@dp.callback_query(lambda cb: cb.data.startswith('current_session'))
async def edit_task(cb: CallbackQuery):
    _, task_str = cb.data.split(':')
    task_id = int(task_str)

    last_task = await db.get_last_task()

    if task_id == 0:
        last_task_start = datetime.combine (last_task.date, last_task.time)
        await db.close_last_task (
            time_start=last_task_start,
            session_id=last_task.session_id
        )
        await cb.answer (f'Отдыхаем')

    else:
        if last_task and not last_task.duration:
            last_task_start = datetime.combine (last_task.date, last_task.time)
            await db.close_last_task(
                time_start=last_task_start,
                session_id=last_task.session_id
            )

        await db.start_new_session(task_id)
        await cb.answer(f'Начал!')

    text = await get_start_text ()
    tasks = await db.get_all_task ()

    await cb.message.edit_text (text, reply_markup=kb.get_start_kb (tasks))


# отменяет действие
@dp.callback_query(lambda cb: cb.data.startswith('cancel'))
async def edit_task(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
