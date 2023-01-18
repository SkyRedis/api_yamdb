from django.urls import path, include
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

router_api_v1 = routers.DefaultRouter()

router_api_v1.register('users', ...)  # get, post, get_id, patch_id, del. Права доступа: Администратор
router_api_v1.register('users/me', ...)  # get, patch Получение данных своей учетной записи. Права доступа: is_authorized
router_api_v1.register('titles', TitleViewSet, basename='titles')
router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),  # Разве нам нужен тут re_path? У нас пока нет регулярных выражений.
    path('v1/auth/token/', ....as_view(), name='get_token'),  # Получение JWT-токена
    path('v1/auth/signup/', ....as_view(), name='signup'),  # Регистрация нового пользователя
]
