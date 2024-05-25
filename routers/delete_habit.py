from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form


delete_habit_router = Router()


@delete_habit_router.message(Form.buttons, F.text == ButtonText.DELETE_HABIT)
async def handle_delete_habit(message: types.Message):
    """Handle deleting habits."""
    await message.answer(
        text="Перешли обработчик удаления привычек\n",
        reply_markup=ReplyKeyboardRemove(),
    )
