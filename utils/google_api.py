import gspread
import logging
import asyncio

from gspread.spreadsheet import Spreadsheet

from init import FILE_GOOGLE, TABLE_ID


# подключение к таблице
def get_google_connect() -> Spreadsheet:
    gc = gspread.service_account (filename=FILE_GOOGLE)
    return gc.open_by_key (TABLE_ID)


# возвращает номер последней свободной строки
def search_last_row(sh: Spreadsheet) -> int:
    id_column = sh.get_worksheet(1).col_values(1)
    while not len(id_column[-1]) > 0:
        id_column = id_column[-1]
    return len (id_column) + 1


# дневной отчёт
async def send_daily_report_in_table(data: list[list]):
    if len(data) > 0:
        sh = get_google_connect ()
        last_row = search_last_row(sh)
        await asyncio.sleep(1)

        cell = f'a{last_row}:c{last_row + len(data) - 1}'
        sh.get_worksheet (1).update (cell, data)


# дневной отчёт
async def send_global_report_in_table(data: list[list]):
    if len(data) > 0:
        sh = get_google_connect ()

        cell = f'a2:b{len(data) + 1}'
        sh.get_worksheet (2).update (cell, data)


