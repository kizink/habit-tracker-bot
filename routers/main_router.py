from aiogram import Router

from .start_dialogue import start_dialogue_router
from .add_habit import add_habit_router
from .delete_habit import delete_habit_router
from .show_habits import show_habits_router
from .unknown_message import unknown_message_router
from .save_history import save_history_router
from .show_history import show_history_router


router = Router()


router.include_routers(
    start_dialogue_router,
    show_habits_router,
    add_habit_router,
    delete_habit_router,
    save_history_router,
    show_history_router,
    unknown_message_router,
)
