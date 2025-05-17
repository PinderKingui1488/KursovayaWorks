from celery import shared_task

from habit.services import send_telegram_message


@shared_task
def habit_remind(habit):
    message = f'будильник на привычка"{habit}"'
    if habit.is_enjoyable:
        send_telegram_message(habit.owner.tg_id, message)
    else:
        message += f", приз забери амогус {habit.reward if habit.reward else habit.related_message}"
        send_telegram_message(habit.owner.tg_id, message)
