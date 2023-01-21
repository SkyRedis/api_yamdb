from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import UserSignupSerializer, UserSerializer
from reviews.models import User


class UserViewset(ModelViewSet):
    """
    GET: Получить список всех пользователей. Права доступа: Администратор
    POST: Добавить нового пользователя. Права доступа: Администратор
          Поля email и username должны быть уникальными.
    GET: Получить пользователя по username. Права доступа: Администратор
    PATCH: Изменить данные пользователя по username. Права доступа:
           Администратор. Поля email и username должны быть уникальными.
    GET: Получить данные своей учетной записи Права доступа:
         Любой авторизованный пользователь
    PATCH: Изменить данные своей учетной записи Права доступа:
         Любой авторизованный пользователь
         Поля email и username должны быть уникальными.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            if request and hasattr(request, "user"):
                user = request.user
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            user = get_object_or_404(User, username="admin5")
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(password='change_me')


class UserSignupViewset(CreateModelMixin, GenericViewSet):
    """
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    """
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )

    def perform_create(self, serializer):
        serializer.save(password='change_me')
