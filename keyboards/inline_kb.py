from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

import db


# поиск
def get_start_kb(tasks: tuple) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔄 Обновить', callback_data='back_start')
    kb.button(text='⏸ Перерыв', callback_data='current_session:0')
    kb.button(text='⛔ На сегодня всё', callback_data='report_daily')

    for task in tasks:
        kb.button(text=task.name, callback_data=f'current_session:{task.id}')

    kb.adjust(3, 1)
    return kb.as_markup()


# поиск
def get_edit_task_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='➕ Добавить', callback_data='add_task')
    kb.button(text='✅ Завершить', callback_data='inactive_task:choice')
    kb.adjust(1)
    return kb.as_markup()


# делает задачу неактивной
def get_make_inactive_task_kb(tasks: tuple[db.TaskRow]):
    kb = InlineKeyboardBuilder ()
    for task in tasks:
        kb.button(text=task.name, callback_data=f'inactive_task:{task.id}')

    kb.button(text='🔙 Назад', callback_data='back_edit_task')

    kb.adjust(1)
    return kb.as_markup()


# отмена
def get_cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')]])
