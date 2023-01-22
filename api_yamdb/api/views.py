import secrets
import string

from rest_framework import filters, permissions, viewsets, views, exceptions
from rest_framework_simplejwt.serializers import SlidingToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate

from reviews.models import Category, Genre, Title, Comment, Review, User

from .serializers import (
    CategorySerializer, GenreSerializer,
    CommentSerializer, ReviewSerializer,
    UserSignupSerializer, UserSerializer,
    TitleListSerializer, TitleCreateSerializer,
    TokenRequestSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """Список категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=category__name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Список жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=genre__name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Список произведений"""
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.action == 'list':
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            queryset = Review.objects.all().filter(
                title_id=title.id
            )
        else:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            queryset = title.objects.all().filter(
                title_id=title.id,
                id=self.kwargs.get('review_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.action == 'list':
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            review = Review.objects.all().filter(
                title_id=title.id,
                id=self.kwargs.get('review_id')
            )
            queryset = Review.objects.all().filter(
                review_id=review.id
            )
        else:
            title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
            review = Review.objects.all().filter(
                title_id=title.id,
                id=self.kwargs.get('review_id')
            )
            queryset = Comment.objects.all().filter(
                review_id=review.id,
                id=self.kwargs.get('comment_id')
            )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = Review.objects.all().filter(
                title_id=title.id,
                id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


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
    USER_ROLES = ('user'),
                 ('moderator'),
                 ('admin'),
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            user = request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))

            user = serializer.save()
            user.set_password(password)
            user.save()

            send_mail(
                '"YAMDB". Registration confirmation',  # "Тема"
                (f'Уважаемый {user.username},'
                 ' ваш код подтверждения: {password}.'),  # "Текст"
                'admin@yamdb.com',  # "От кого"
                [f'{user.email}'],  # "Кому"
                fail_silently=False,
            )


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
        if serializer.is_valid():
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))

            user = serializer.save()
            user.set_password(password)
            user.save()

            send_mail(
                '"YAMDB". Registration confirmation',  # "Тема"
                (f'Уважаемый {user.username},'
                 ' ваш код подтверждения: {password}.'),  # "Текст"
                'admin@yamdb.com',  # "От кого"
                [f'{user.email}'],  # "Кому"
                fail_silently=False,
            )


class APIGetToken(views.APIView):
    """
    Запрос токена для зарегистрированного пользователя.
    1. POST-запрос с обязательными параметрами 'username' и 'confirmation_id'
       на эндпоинт /api/v1/auth/token/.
    2. Аутентифицированному пользователю возвращается токен: Bearer.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data_serializer = TokenRequestSerializer(data=request.data)

        data_serializer.is_valid(raise_exception=True)
        username = data_serializer.validated_data['username']
        password = data_serializer.validated_data['confirmation_id']

        user = authenticate(username=username, password=password)

        if user is not None:
            token = SlidingToken.for_user(user)
            response = {'token': str(token)}

            return Response(response)
        raise exceptions.AuthenticationFailed('Check your confirmation_id')
