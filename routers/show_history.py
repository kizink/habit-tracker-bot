import calendar
import datetime
import aiogram.utils.formatting

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.common_keyboards import ButtonText
from .FSM_states import Form
from db import db_scripts


show_history_router = Router()


def _format_actions(actions: list[db_scripts.Action]) -> str:
    curr_dt = datetime.datetime.now()
    year = curr_dt.year
    month = curr_dt.month
    month_str = calendar.month(year, month, w=4, l=2)
    month_str = month_str.replace("\n", "  \n")
    for action in actions:
        if action.action_time.year != year\
                or action.action_time.month != month:
            continue
        day_pattern = " " + str(action.action_time.day)
        emoji = "✅" if action.is_complited else "❌"
        month_str = month_str.replace(day_pattern + "  ", day_pattern + emoji)
    result = aiogram.utils.formatting.Pre(month_str)
    return result


@show_history_router.message(Form.buttons, F.text == ButtonText.SHOW_HISTORY)
async def handle_show_history(
    message: Message, state: FSMContext, db: db_scripts.DataBase
) -> None:
    """Handle showing history."""
    habits = db.get_habits(message.from_user.id)
    if len(habits) == 0:
        content = aiogram.utils.formatting.Text("No habits")
        await message.answer(**content.as_kwargs())
        return
    content = []
    for habit in habits:
        actions = db.get_actions(habit.id)
        formatted_actions = _format_actions(actions)
        formatted_title = aiogram.utils.formatting.Bold(habit.name)
        content_item = aiogram.utils.formatting.as_section(
            formatted_title, formatted_actions)
        content.append(content_item)
    content = aiogram.utils.formatting.as_list(*content, sep='\n\n')
    await message.answer(**content.as_kwargs())
