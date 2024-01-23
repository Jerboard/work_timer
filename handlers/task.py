from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


import json
from datetime import datetime

import db
from init import dp, TZ, bot
from keyboards import inline_kb as kb
from utils.texts import get_start_text


# команда старт
@dp.message(Command('edit_task'))
async def com_start(msg: Message, state: FSMContext):
    await state.clear()
    text = 'Выбор действия'
    await msg.answer(text, reply_markup=kb.get_edit_task_kb())


# возвращает к начинает задачу
@dp.callback_query(lambda cb: cb.data.startswith('back_edit_task'))
async def new_task(cb: CallbackQuery, state: FSMContext):
    await state.clear ()
    text = 'Выбор действия'
    await cb.message.edit_text (text, reply_markup=kb.get_edit_task_kb ())


# начинает задачу
@dp.callback_query(lambda cb: cb.data.startswith('add_task'))
async def new_task(cb: CallbackQuery, state: FSMContext):
    await state.set_state('add_task')
    sent = await cb.message.answer('Название задачи', reply_markup=kb.get_cancel_kb())
    await state.update_data (data={
        'base_message_id': cb.message.message_id,
        'back_message_id': sent.message_id
    })


# принимает название, добавляет задачу
@dp.message(StateFilter('add_task'))
async def add_new_task(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.clear()

    added = await db.add_task(user_id=msg.from_user.id, name=msg.text)

    if added:

        await bot.delete_message(chat_id=msg.chat.id, message_id=data['back_message_id'])

        tasks = await db.get_all_task ()
        text = await get_start_text ()
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=data['base_message_id'],
            text=text,
            reply_markup=kb.get_start_kb(tasks)
        )
    else:
        await msg.answer('Не удалось')


# отключить задачу
@dp.callback_query(lambda cb: cb.data.startswith('inactive_task'))
async def new_task(cb: CallbackQuery, state: FSMContext):
    _, task_id = cb.data.split(':')

    if task_id == 'choice':
        tasks = await db.get_all_task ()
        await cb.message.edit_text('Выберите задачу', reply_markup=kb.get_make_inactive_task_kb(tasks))

    else:
        await db.update_task(task_id=int(task_id), status='done')
        text = 'Выбор действия'
        await cb.message.edit_text (text, reply_markup=kb.get_edit_task_kb())
