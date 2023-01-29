import secrets
import string
from http import HTTPStatus

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, generics, permissions, views,
                            viewsets)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import Categories, Comments, Genres, IsAdmin, Reviews, Titles
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          TokenRequestSerializer, UserSerializer,
                          UserSignupSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    """Список категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (Categories,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Список жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (Genres,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Список произведений"""
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (Titles,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (Reviews,)
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Review.objects.all().filter(
            title_id=self.kwargs.get('title_id'),
        ).order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (Comments,)
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Comment.objects.all().filter(
            review_id=self.kwargs.get('review_id')
        ).order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = Review.objects.all().filter(
            title_id=title.id,
            id=self.kwargs.get('review_id')
        )[0]
        serializer.save(author=self.request.user, review_id=review)


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
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(None)
            user.save()


class UserSignupView(views.APIView):
    """
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)

        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))

        user.set_password(password)
        user.save()

        send_mail(
            '"YAMDB". Registration confirmation',  # "Тема"
            f'Usernsme: {username}, confirmation_code: {password}',  # "Текст"
            'admin@yamdb.com',  # "От кого"
            [f'{user.email}'],  # "Кому"
            fail_silently=False,
        )

        return Response(serializer.data, status=HTTPStatus.OK)


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except AttributeError:
            raise exceptions.NotFound

    def put(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PUT')

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save(role=user.role)

        return Response(serializer.data)


class GetTokenView(views.APIView):
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
        password = data_serializer.validated_data['confirmation_code']

        user = authenticate(username=username, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            response = {'token': str(token.access_token)}

            return Response(response)
        raise exceptions.ValidationError('Check your confirmation_id')
