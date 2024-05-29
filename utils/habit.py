from db.db_scripts import Habit


def pretty_formatting(habit: Habit, proxy_id: int) -> str:
    """Return a nicely formatted habit string."""
    id = "<b>Привычка</b> " + str(proxy_id) + "\n"
    name = "<i>Название привычки</i>: " + habit.name + "\n"
    description = "<i>Описание привычки</i>: " + habit.description + "\n"
    notification_time = "<i>Время уведомления</i>: "\
        + habit.notification_time.strftime('%H:%M') + "\n"

    return id + name + description + notification_time
