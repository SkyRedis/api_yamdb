from django.urls import path, include
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

router_api_v1 = routers.DefaultRouter()

router_api_v1.register('titles', TitleViewSet, basename='titles')
router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),  # Разве нам нужен тут re_path? У нас пока нет регулярных выражений.
]
