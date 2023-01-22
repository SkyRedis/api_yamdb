from rest_framework import serializers, validators, exceptions

from reviews.models import (
    Category, Genre, Title, GenreTitle, Comment, Review, User
)


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователя
    1. POST-запрос с обязательными параметрами 'email' и 'username'
       на эндпоинт /api/v1/auth/signup/.
    2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code)
       на указанный адрес email.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise exceptions.ValidationError('Do not use "me" as username')
        return super().validate(attrs)

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """
    Создание пользователя (администратором)
    Редактирование пользователя
    Ендпоинт /api/v1/users
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise exceptions.ValidationError('Do not use "me" as username')
        return super().validate(attrs)

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User


class TokenRequestSerializer(serializers.Serializer):
    """
    Запрос токена для зарегистрированного пользователя.
    1. POST-запрос с обязательными параметрами 'username' и 'confirmation_id'
       на эндпоинт /api/v1/auth/token/.
    2. Аутентифицированному пользователю возвращается токен: Bearer.
    """
    username = serializers.CharField(required=True)
    confirmation_id = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise exceptions.NotFound(f'User {attrs["username"]} not found')

        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title

        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title


class CommentSerializer(serializers.ModelSerializer):

    class Meta():
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta():
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
