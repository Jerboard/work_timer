from aiogram.types import ErrorEvent, Message

from init import dp, bot, DEBUG, log_error


@dp.errors()
async def error_handler(ex: ErrorEvent):
    log_error (ex.exception)
