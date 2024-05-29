import aiogram.utils.formatting

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form
from db import db_scripts
from utils.habit import pretty_formatting as pretty


show_habits_router = Router()


@show_habits_router.message(Form.buttons, F.text == ButtonText.SHOW_HABITS)
async def handle_show_habits(message: Message, state: FSMContext,
                             db: db_scripts.DataBase) -> None:
    """Handle showing habits."""
    habits = db.get_habits(message.from_user.id)
    content = aiogram.utils.formatting.Text("Нет превычек")
    if len(habits) > 0:
        content = [pretty(habits[i], i) for i in range(len(habits))]
    await message.answer('\n'.join(content), parse_mode=ParseMode.HTML)
