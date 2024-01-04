from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


# поиск
def get_start_kb(tasks: tuple) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='➕ Новая задача', callback_data='add_task')
    kb.button(text='⏸ Перерыв', callback_data='current_session:0')
    kb.button(text='⛔ На сегодня всё', callback_data='report_daily')

    for task in tasks:
        kb.button(text=task.name, callback_data=f'current_session:{task.id}')

    kb.adjust(3, 1)
    return kb.as_markup()


# отмена
def get_cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')]])
