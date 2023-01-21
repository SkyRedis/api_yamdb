from rest_framework import serializers, validators
from reviews.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Ресурс auth: аутентификация
    1. Пользователь отправляет POST-запрос с параметрами email и username
       на эндпоинт /api/v1/auth/signup/.
    2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code)
       на указанный адрес email. - НЕ РЕАЛИЗОВАНО
    """
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """
    Ресурс users: пользователи
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User
