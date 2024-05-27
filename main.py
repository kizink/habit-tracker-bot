import asyncio
import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from routers.main_router import router as main_router
from middlewares.db import DatabaseMiddleware
from db import db_scripts
from notifier import Notifier
from bot_secrets.token import TOKEN


async def main():
    """Configure bot."""
    dp = Dispatcher()
    dp.include_router(main_router)
    db_instance = db_scripts.DataBase()
    dp.update.middleware(DatabaseMiddleware(db=db_instance))
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    notifier = Notifier(bot, db_instance, 60)
    notifier.start()
    await dp.start_polling(bot)
    await notifier.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
    )
    asyncio.run(main())
