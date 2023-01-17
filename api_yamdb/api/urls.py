from django.urls import path, include, re_path
from rest_framework import routers

from api.views import ...

router_api_v1 = routers.DefaultRouter()

router_api_v1.register(r'v1/users', ...)  # get, post, get_id, patch_id, del. Права доступа: Администратор
router_api_v1.register(r'v1/users/me', ...)  # get, patch Получение данных своей учетной записи. Права доступа: is_authorized
router_api_v1.register(r'v1/...', ...)
router_api_v1.register(r'v1/...', ...)

urlpatterns = [
    re_path('', include(router_api_v1.urls)),
    path('v1/auth/token/', ....as_view(), name='get_token'),  # Получение JWT-токена
    path('v1/auth/signup/', ....as_view(), name='signup'),  # Регистрация нового пользователя
]
