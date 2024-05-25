from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form


add_habit_router = Router()


@add_habit_router.message(Form.buttons, F.text == ButtonText.ADD_HABIT)
async def handle_add_habit(message: types.Message):
    """Handle adding habits."""
    await message.answer(
        text="Перешли обработчик добавления привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )
