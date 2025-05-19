from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        # Проверка времени выполнения
        if "duration_to_complete" in data and data["duration_to_complete"] > 120:
            raise ValidationError("время максимум 2 пачки пельмений сварить")
        
        # Проверка периодичности
        if "periodicity" in data and data["periodicity"] is not None and data["periodicity"] > 7:
            raise ValidationError("кд 7 суток ")

        # Проверка связанной привычки
        if "related_habit" in data and data["related_habit"]:
            related_habit = data["related_habit"]
            if not related_habit.is_enjoyable:
                raise ValidationError("Связанная привычка должна быть приятной")
            if data.get("is_enjoyable", False):
                raise ValidationError("Приятная привычка не может иметь связанную привычку")

        # Проверка награды и связанной привычки
        if "bonus" in data and data["bonus"] and "related_habit" in data and data["related_habit"]:
            raise ValidationError("Нельзя одновременно указывать и награду, и связанную привычку")

        # Проверка приятной привычки
        if data.get("is_enjoyable", False):
            if "bonus" in data and data["bonus"]:
                raise ValidationError("У приятной привычки не может быть награды")
            if "related_habit" in data and data["related_habit"]:
                raise ValidationError("У приятной привычки не может быть связанной привычки")

        return data
