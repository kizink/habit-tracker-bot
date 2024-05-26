from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import common_keyboards
from keyboards.common_keyboards import ButtonText
from .FSM_states import Form
from db import db_scripts


show_habits_router = Router()


@show_habits_router.message(Form.buttons, F.text == ButtonText.SHOW_HABITS)
async def handle_show_habits(message: Message, state: FSMContext,
                             db: db_scripts.DataBase) -> None:
    """Handle showing habits."""
    await message.answer(
        text="Перешли обработчик показа привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(str(db.get_habits(message.from_user.id)))

    await message.answer("Выберите действие",
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)
