from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    """States of FSM."""

    greetings = State()
    getName = State()
    menu = State()
    buttons = State()
