from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from datetime import datetime

import traceback
import logging
import os
import re

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
        BotCommand (command='/start', description='Меню'),
        BotCommand (command='/edit_task', description='Таски'),
        BotCommand (command='/pass_gen', description='Создать пароль'),
    ]

    await bot.set_my_commands (main_menu_commands)


def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        tb = ''
        start_row = '  File "C:' if DEBUG else '  File'
        tb_split = ex_traceback.split('\n')
        for row in tb_split:
            if row.startswith(start_row) and not re.search ('venv', row):
                tb += f'{row}\n'

        msg = ex_traceback.split ('\n\n') [-1]
        logging.warning(f'{now}\n{tb}\n{msg}\n---------------------------------\n')
    else:
        logging.warning(f'{now}\n{message}\n\n---------------------------------\n')

