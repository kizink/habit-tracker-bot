from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import common_keyboards
from keyboards.common_keyboards import ButtonText
from .FSM_states import Form, DeleteHabitStates
from db import db_scripts


delete_habit_router = Router()


@delete_habit_router.message(Form.buttons, F.text == ButtonText.DELETE_HABIT)
async def handle_delete_habit(message: Message, state: FSMContext,
                              db: db_scripts.DataBase) -> None:
    """Handle deleting habits."""
    await message.answer(
        text=str(db.get_habits(message.from_user.id)),
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Введите id привычки, которую хотите удалить")
    await state.set_state(DeleteHabitStates.ChoiceHabits)


@delete_habit_router.message(DeleteHabitStates.ChoiceHabits)
async def handle_choice_habits(message: Message, state: FSMContext,
                               db: db_scripts.DataBase) -> None:
    """Choice habbits to delete."""
    db.delete_habit(int(message.text))
    await message.answer("Привычка с id = " + message.text + " удалена")

    await message.answer("Выберите действие",
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)
