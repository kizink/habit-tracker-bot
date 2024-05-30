from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import common_keyboards
from keyboards.common_keyboards import ButtonText
from .FSM_states import Form, AddHabitStates
from db import db_scripts
from utils.translation import _


add_habit_router = Router()


@add_habit_router.message(Form.buttons, F.text == ButtonText.ADD_HABIT)
async def handle_add_habit(message: Message, state: FSMContext) -> None:
    """Handle adding habits."""
    await message.answer(
        _("Введите название привычки"),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddHabitStates.getName)


@add_habit_router.message(AddHabitStates.getName)
async def getNameHabit(message: Message, state: FSMContext) -> None:
    """Get habit name."""
    await state.update_data(habit_name=message.text)

    await state.set_state(AddHabitStates.getDescription)
    await message.answer(_("Введите описание привычки"))


@add_habit_router.message(AddHabitStates.getDescription)
async def getDescriptionHabit(message: Message, state: FSMContext) -> None:
    """Get habit description."""
    await state.update_data(description_name=message.text)

    await state.set_state(AddHabitStates.getNotificationTime)
    await message.answer(
        _("Введите время, в которое напомнить вам о привычке")
    )


@add_habit_router.message(AddHabitStates.getNotificationTime)
async def getNotificationTime(message: Message, state: FSMContext,
                              db: db_scripts.DataBase) -> None:
    """Get habit notification time."""
    await state.update_data(notification_time=message.text)
    await state.set_state(AddHabitStates.inputConfirmation)
    await inputConfirmation(message, state, db)


@add_habit_router.message(AddHabitStates.inputConfirmation)
async def inputConfirmation(message: Message, state: FSMContext,
                            db: db_scripts.DataBase) -> None:
    """Save habit data to db."""
    data = await state.get_data()

    user_id = message.from_user.id
    habit_name = data["habit_name"]
    descr = data["description_name"]
    time = data["notification_time"]
    await state.clear()
    db.add_habit(user_id, habit_name, descr, time)

    await message.answer(_("Выберите действие"),
                         reply_markup=common_keyboards.get_menu_kb())
    await state.set_state(Form.buttons)
