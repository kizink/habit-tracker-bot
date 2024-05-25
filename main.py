import asyncio
import logging
import sys
from bot_secrets.token import TOKEN

from aiogram import Bot, Dispatcher, F, Router, html, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove
)
from keyboards import common_keyboards
from keyboards.common_keyboards import ButtonText
import db

example_db = db.DataBase()
form_router = Router()


class Form(StatesGroup):
    """States of FSM."""

    greetings = State()
    getName = State()
    menu = State()
    buttons = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    """Run when you type /start."""
    if not example_db.user_exists(message.from_user.id):
        await state.set_state(Form.greetings)
        await process_name(message, state)
    else:
        await state.set_state(Form.menu)
        await menu(message, state)


@form_router.message(Form.greetings)
async def process_name(message: Message, state: FSMContext) -> None:
    """Get a name."""
    await message.answer("Привет! Как тебя зовут?",)
    await state.set_state(Form.getName)


@form_router.message(Form.getName)
async def saving_name(message: Message, state: FSMContext) -> None:
    """Save name to DB."""
    example_db.add_user(message.from_user.id, message.text)

    await state.set_state(Form.menu)
    await message.answer(
        f"Приятно познакомиться, {html.quote(message.text)}!\n",
    )
    await menu(message, state)


@form_router.message(Form.menu)
async def menu(message: Message, state: FSMContext) -> None:
    """Show menu_keyboard."""
    await message.answer("Выберите действие",
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)


@form_router.message(Form.buttons, F.text == ButtonText.ADD_HABIT)
async def handle_add_habit(message: types.Message):
    """Handle adding habits."""
    await message.answer(
        text="Перешли обработчик добавления привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.buttons, F.text == ButtonText.DELETE_HABIT)
async def handle_delete_habit(message: types.Message):
    """Handle deleting habits."""
    await message.answer(
        text="Перешли обработчик удаления привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.buttons, F.text == ButtonText.SHOW_HABITS)
async def handle_show_habits(message: types.Message):
    """Handle showing habits."""
    await message.answer(
        text="Перешли обработчик показа привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    """Configure bot."""
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
