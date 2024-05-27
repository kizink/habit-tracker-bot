import aiogram.utils.formatting

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form
from db import db_scripts


show_habits_router = Router()


@show_habits_router.message(Form.buttons, F.text == ButtonText.SHOW_HABITS)
async def handle_show_habits(message: Message, state: FSMContext,
                             db: db_scripts.DataBase) -> None:
    """Handle showing habits."""
    habits = db.get_habits(message.from_user.id)
    content = aiogram.utils.formatting.Text("No habits")
    if len(habits) > 0:
        content = aiogram.utils.formatting.as_list(*habits, sep='\n\n')
    await message.answer(**content.as_kwargs())
