from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form


show_habits_router = Router()


@show_habits_router.message(Form.buttons, F.text == ButtonText.SHOW_HABITS)
async def handle_show_habits(message: types.Message):
    """Handle showing habits."""
    await message.answer(
        text="Перешли обработчик показа привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )
