import asyncio
import logging
import sys
from bot_secrets.token import TOKEN

from aiogram import Bot
from aiogram import Dispatcher

from aiogram.enums import ParseMode

from routers.main_router import router as main_router
from middlewares.db import DatabaseMiddleware
from db import db_scripts


async def main():
    """Configure bot."""
    dp = Dispatcher()
    dp.include_router(main_router)

    db_instance = db_scripts.DataBase()
    dp.update.middleware(DatabaseMiddleware(db=db_instance))

    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
