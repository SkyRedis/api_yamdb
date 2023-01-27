from django.db.models import Avg
from rest_framework import exceptions, serializers, validators
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователя
    1. POST-запрос с обязательными параметрами 'email' и 'username'
       на эндпоинт /api/v1/auth/signup/.
    2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code)
       на указанный адрес email.
    """
    username = serializers.RegexField(
        r"^[\w.@+-]+\Z",
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise exceptions.ValidationError(
                {'username': ('Do not use "me" as username')})

        user = User.objects.filter(username=attrs['username'],
                                   email=attrs['email'])
        if user.exists():
            """if user[0].has_usable_password():
                raise exceptions.ValidationError(
                    {'username': 'User is already registered'})"""
            return super().validate(attrs)

        if User.objects.filter(username=attrs['username']).exists():
            raise exceptions.ValidationError(
                {'username': 'This field must be unique.'})

        if User.objects.filter(email=attrs['email']):
            raise exceptions.ValidationError(
                {'email': 'This field must be unique.'})

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
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        if 'username' in attrs and attrs['username'] == 'me':
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
    confirmation_code = serializers.CharField(required=True)

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
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(
        many=True)
    category = serializers.StringRelatedField(
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        reviews = Review.objects.all().filter(
            title_id=obj.id
        )
        rating = reviews.aggregate(Avg('score'))
        return int(list(rating.values())[0])


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        reviews = Review.objects.all().filter(
            title_id=obj.id
        )
        rating = reviews.aggregate(Avg('score'))
        return int(list(rating.values())[0])


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta():
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        lookup_field = 'id'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta():
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        lookup_field = 'id'
