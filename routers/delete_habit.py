import aiogram.utils.formatting

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from keyboards import common_keyboards
from keyboards.common_keyboards import ButtonText
from .FSM_states import Form, DeleteHabitStates
from db import db_scripts
from utils.habit import pretty_formatting as pretty
from utils.translation import _


delete_habit_router = Router()


@delete_habit_router.message(Form.buttons, F.text == ButtonText.DELETE_HABIT)
async def handle_delete_habit(message: Message, state: FSMContext,
                              db: db_scripts.DataBase) -> None:
    """Handle deleting habits."""
    habits = db.get_habits(message.from_user.id)
    if len(habits) == 0:
        content = aiogram.utils.formatting.Text(_("Нет привычек"))
        await message.answer(**content.as_kwargs())
        return
    await state.update_data(habit_list=habits)

    content = [pretty(habits[i], i) for i in range(len(habits))]
    await message.answer('\n'.join(content), parse_mode=ParseMode.HTML)
    await message.answer(_("Введите номер привычки, которую хотите удалить"))
    await state.set_state(DeleteHabitStates.ChoiceHabits)


@delete_habit_router.message(DeleteHabitStates.ChoiceHabits)
async def handle_choice_habits(message: Message, state: FSMContext,
                               db: db_scripts.DataBase) -> None:
    """Choice habbits to delete."""
    data = await state.get_data()
    habits = data["habit_list"]
    db.delete_habit(habits[int(message.text)].id)

    await message.answer(_("Привычка с номером = ")
                         + message.text + _(" удалена"))
    await state.clear()

    await message.answer(_("Выберите действие"),
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)
