from django.db import models
from users.models import User


class HabitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Habit(models.Model):
    """
    Модель привычки пользователя
    """
    objects = HabitManager()
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name="крафт обилки")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="место и время для исполнения ")
    scheduled_time = models.TimeField(verbose_name="время на покушать ", auto_now=False, auto_now_add=False)
    activity = models.CharField(max_length=100, verbose_name="цель")
    is_enjoyable = models.BooleanField(default=False, blank=True, null=True,
                                              verbose_name="талант от привычки")
    related_habit = models.ForeignKey(to="self", on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name="привязка привычка")
    periodicity = models.PositiveIntegerField(verbose_name="таймаут")
    bonus = models.CharField(max_length=100, blank=True, null=True, verbose_name="приз")
    duration_to_complete = models.PositiveIntegerField(default=120, verbose_name="время работы")
    is_habit_public = models.BooleanField(default=False, blank=True, null=True, verbose_name="общий признак")

    def __str__(self):
        return f"{self.activity}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        app_label = 'habit'
