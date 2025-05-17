import json
from datetime import datetime, timedelta

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import BOT_TOKEN


def send_telegram_message(id, message):
    params = {
        "text": message,
        "chat_id": id,
    }
    return requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params
    )


def habit_reminder(habit):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.periodicity,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name="Habit reminder",
        task="habits.tasks.habit_remind",
        kwargs=json.dumps(
            {
                "be_careful": True,
            }
        ),
        expires=datetime.now() + timedelta(seconds=habit.time_to_complete),
    )
