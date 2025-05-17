from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer


class UserCreateApi(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
