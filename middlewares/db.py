from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
import db


class DatabaseMiddleware(BaseMiddleware):
    """middleware for working with a db."""

    def __init__(self, db: db.DataBase) -> None:
        """Init."""
        self.db = db

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]],
                              Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
        """Save db to dict."""
        data['db'] = self.db
        return await handler(event, data)
