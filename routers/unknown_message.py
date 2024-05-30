from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import common_keyboards
from .FSM_states import Form
from utils.translation import _


unknown_message_router = Router()


@unknown_message_router.message()
async def handle_unknown_message(message: Message, state: FSMContext) -> None:
    """Handle unknown message."""
    await message.answer(
        text=_("Нераспознанная команда:") + " " + message.text,
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=_("Выберите действие"),
        reply_markup=common_keyboards.get_menu_kb()
    )
    await state.set_state(Form.buttons)
