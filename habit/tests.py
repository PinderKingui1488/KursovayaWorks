from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email="test@example.com")
        self.test_habit = Habit.objects.create(
            owner=self.test_user,
            location="At home",
            scheduled_time="18:30",
            activity="Do breathing exercises",
            is_enjoyable=True,
            related_habit=None,
            periodicity=1,
            bonus="Fresh air in lungs!",
            duration_to_complete=120,
            is_habit_public=False
        )
        self.client.force_authenticate(user=self.test_user)

    def test_create_habit(self):
        self.assertEqual(Habit.objects.count(), 1)

    def test_retrieve_habit(self):
        url = reverse("habit:habit-detail", args=[self.test_habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("periodicity"), self.test_habit.periodicity)

    def test_list_habits(self):
        url = reverse("habit:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        url = reverse("habit:habit-detail", args=[self.test_habit.pk])
        update_data = {
            "location": "In the kitchen",
            "scheduled_time": "18:30",
            "activity": "Take pills",
            "is_enjoyable": False,
            "periodicity": 1,
            "bonus": "Take medicine on time",
            "duration_to_complete": 120
        }
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("location"), "In the kitchen")

    def test_delete_habit(self):
        url = reverse("habit:habit-detail", args=[self.test_habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habit_list(self):
        url = reverse("habit:habit-public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
