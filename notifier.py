import asyncio
import datetime
import logging

from contextlib import suppress
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from db.db_scripts import DataBase, Habit


class Notifier():
    """Process sending notifications."""

    def __init__(self, bot: Bot, db: DataBase, period: int):
        """Save parameters."""
        self.bot = bot
        self.db = db
        self.is_running = False
        self.period = period
        self._task = None
        self.logger = logging.getLogger(__name__)

    async def send_notiffication(self, habit: Habit):
        """Send notification about habit."""
        self.logger.debug(f'Send notification for {habit}')
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(
            text="✅",
            callback_data=f"notify_{habit.id}_yes")
        )
        builder.add(InlineKeyboardButton(
            text="❌",
            callback_data=f"notify_{habit.id}_no")
        )
        try:
            await self.bot.send_message(
                chat_id=habit.user_id,
                text=habit.name,
                reply_markup=builder.as_markup()
            )
        except Exception:
            self.logger.info(f'Failed send notification for {habit}')

    async def _check_and_notify(self):
        curr_dt = datetime.datetime.now()
        time_range = datetime.timedelta(seconds=self.period/2)
        notify_from = (curr_dt - time_range).time()
        notify_to = (curr_dt + time_range).time()
        habits = self.db.get_habits_for_notification(notify_from, notify_to)
        self.logger.info(f'Found {len(habits)} habits for notification')
        for habit in habits:
            asyncio.ensure_future(self.send_notiffication(habit))

    async def _run(self):
        while True:
            try:
                await self._check_and_notify()
            except Exception as e:
                self.logger.error(f'check_and_notify failed. Exception: {e}')
            await asyncio.sleep(self.period)

    def start(self):
        """Start an asynchronous task."""
        if not self.is_running:
            self.is_running = True
            self._task = asyncio.ensure_future(self._run())
            self.logger.info('Notifier started')
        else:
            self.logger.warning('Notifier already started')

    async def stop(self):
        """Stop an asynchronous task."""
        if self.is_running:
            self.is_running = False
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self.logger.info('Notifier stopped')
        else:
            self.logger.warning('Notifier already stopped')
