from api.views import CommentViewSet, ReviewViewSet
from django.urls import include, path, re_path
from rest_framework import routers

router_api_v1 = routers.DefaultRouter()

router_api_v1.register(r'v1/users', ...)  # get, post, get_id, patch_id, del. Права доступа: Администратор
router_api_v1.register(r'v1/users/me', ...)  # get, patch Получение данных своей учетной записи. Права доступа: is_authorized
router_api_v1.register(
    r'v1/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router_api_v1.register(
    r'v1/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    re_path('', include(router_api_v1.urls)),
    path('v1/auth/token/', ....as_view(), name='get_token'),  # Получение JWT-токена
    path('v1/auth/signup/', ....as_view(), name='signup'),  # Регистрация нового пользователя
]
