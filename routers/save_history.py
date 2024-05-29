from aiogram import F, Router
from aiogram.types import CallbackQuery
from db import db_scripts


save_history_router = Router()


@save_history_router.callback_query(F.data.startswith("notify_"))
async def handle_save_history(
    callback: CallbackQuery,
    db: db_scripts.DataBase
):
    """Handle user reaction to notification."""
    callback_data = callback.data.split("_")
    action = db_scripts.Action(
        habit_id=int(callback_data[1]),
        action_time=callback.message.date,
        is_complited=callback_data[2] == "yes",
    )
    res = db.add_action(action)
    await callback.answer()

    text = "Не удалось сохранить статистику"
    if res:
        text = callback.message.text
        if action.is_complited:
            text += " ✅"
        else:
            text += " ❌"
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.message.bot.edit_message_text(
        text,
        chat_id=chat_id,
        message_id=message_id
    )
