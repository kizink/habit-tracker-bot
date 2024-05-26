from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import common_keyboards
from .FSM_states import Form
from db import db_scripts


start_dialogue_router = Router()


@start_dialogue_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext,
                        db: db_scripts.DataBase) -> None:
    """Run when you type /start."""
    if not db.user_exists(message.from_user.id):
        await state.set_state(Form.greetings)
        await process_name(message, state)
    else:
        await state.set_state(Form.menu)
        await menu(message, state)


@start_dialogue_router.message(Form.greetings)
async def process_name(message: Message, state: FSMContext) -> None:
    """Get a name."""
    await message.answer("Привет! Как тебя зовут?",)
    await state.set_state(Form.getName)


@start_dialogue_router.message(Form.getName)
async def saving_name(message: Message, state: FSMContext,
                      db: db_scripts.DataBase) -> None:
    """Save name to DB."""
    db.add_user(message.from_user.id, message.text)

    await state.set_state(Form.menu)
    await message.answer(
        f"Приятно познакомиться, {html.quote(message.text)}!\n",
    )
    await menu(message, state)


@start_dialogue_router.message(Form.menu)
async def menu(message: Message, state: FSMContext) -> None:
    """Show menu_keyboard."""
    await message.answer("Выберите действие",
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)
