from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ButtonText:
    """Keyboard button text."""

    SHOW_HABITS = "Посмотреть текущие привычки"
    ADD_HABIT = "Добавить привычку"
    DELETE_HABIT = "Удалить привычку"


def get_menu_kb() -> ReplyKeyboardMarkup:
    """Get menu keyboard."""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=ButtonText.SHOW_HABITS))
    builder.add(KeyboardButton(text=ButtonText.ADD_HABIT))
    builder.add(KeyboardButton(text=ButtonText.DELETE_HABIT))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
