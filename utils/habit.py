from db.db_scripts import Habit
from .translation import _


def pretty_formatting(habit: Habit, proxy_id: int) -> str:
    """Return a nicely formatted habit string."""
    id = _("<b>Привычка</b> ") + str(proxy_id) + "\n"
    name = _("<i>Название привычки</i>: ") + habit.name + "\n"
    description = _("<i>Описание привычки</i>: ") + habit.description + "\n"
    notification_time = _("<i>Время уведомления</i>: ")\
        + habit.notification_time.strftime('%H:%M') + "\n"

    return id + name + description + notification_time
