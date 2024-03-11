from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from datetime import datetime

import traceback
import logging

from dotenv import load_dotenv
from os import getenv
from pytz import timezone

from sqlalchemy.ext.asyncio import create_async_engine

import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy (uvloop.EventLoopPolicy ())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop ()
dp = Dispatcher ()
bot = Bot (getenv ("TOKEN"), parse_mode=ParseMode.HTML)

DEBUG = bool(int(getenv('DEBUG')))
TZ = timezone ('Asia/Tbilisi')
DATETIME_STR_FORMAT = '%d.%m.%y %H:%M'
DATE_STR_FORMAT = '%d.%m.%y'

ENGINE = create_async_engine (url=getenv ('DB_URL'))
TABLE_ID = getenv('TABLE_ID')
FILE_GOOGLE = getenv('FILE_GOOGLE')


async def set_main_menu() -> None:
    main_menu_commands = [
        BotCommand (command='/start',
                    description='Меню'),
        BotCommand (command='/edit_task',
                    description='Таски'),
    ]

    await bot.set_my_commands (main_menu_commands)


def log_error(message):
    timestamp = datetime.now (TZ)
    filename = traceback.format_exc () [1]
    line_number = traceback.format_exc () [2]
    logging.error (f'{timestamp} {filename} {line_number}: {message}')

