from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from habit.models import Habit
from habit.paginators import CustomPagination
from habit.serializers import HabitSerializer
from habit.services import habit_reminder
from users.permissions import Owner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
        habit_reminder(habit)

    @action(detail=False, methods=["GET"])
    def public_habits(self, request):
        public_habits = self.queryset.filter(is_habit_public=True)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action not in ["create", "public_habits"]:
            self.permission_classes = (Owner,)
        return super().get_permissions()
