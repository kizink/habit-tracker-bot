from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    """States of FSM."""

    greetings = State()
    getName = State()
    menu = State()
    buttons = State()


class AddHabitStates(StatesGroup):
    """AddHabitStates of FSM."""

    getName = State()
    getDescription = State()
    getNotificationTime = State()
    inputConfirmation = State()


class DeleteHabitStates(StatesGroup):
    """DeleteHabitStates of FSM."""

    showCurrHabits = State()
    ChoiceHabits = State()
    Confirmation = State()
