import asyncio
import logging
import sys


from handlers import dp
from db.base import init_models
from init import set_main_menu, bot, DEBUG


async def main() -> None:
    await init_models()
    await set_main_menu()
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig (level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s", filename='log.log')
    asyncio.run(main())
