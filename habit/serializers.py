from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        if "time_to_complete" in data and data["time_to_complete"] > 120:
            raise ValidationError("время максимум 2 пачки пельмений сварить")
        elif "related_habbit" in data and not (data["is_enjoyable"]):
            raise ValidationError("привычка долджна быть принета , а не отвергнута")
        elif data["is_enjoyable"] and ("reward" in data or "related_habbit" in data):
            raise ValidationError(
                "у такой привычки нет приза , а тока боль страдания "
            )
        elif (
            "periodicity" in data
            and data["periodicity"] is not None
            and data["periodicity"] > 7
        ):
            raise ValidationError("кд 7 суток ")
        return data
