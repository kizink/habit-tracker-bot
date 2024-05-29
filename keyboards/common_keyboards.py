from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.translation import _


class ButtonText:
    """Keyboard button text."""

    SHOW_HABITS = _("Посмотреть текущие привычки")
    ADD_HABIT = _("Добавить привычку")
    DELETE_HABIT = _("Удалить привычку")
    SHOW_HISTORY = _("Посмотреть историю")


def get_menu_kb() -> ReplyKeyboardMarkup:
    """Get menu keyboard."""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=ButtonText.SHOW_HABITS))
    builder.add(KeyboardButton(text=ButtonText.ADD_HABIT))
    builder.add(KeyboardButton(text=ButtonText.DELETE_HABIT))
    builder.add(KeyboardButton(text=ButtonText.SHOW_HISTORY))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
