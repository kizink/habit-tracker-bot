from aiogram import Router

from .start_dialogue import start_dialogue_router
from .add_habit import add_habit_router
from .delete_habit import delete_habit_router
from .show_habits import show_habits_router


router = Router()


router.include_routers(
    start_dialogue_router,
    show_habits_router,
    add_habit_router,
    delete_habit_router,
)
