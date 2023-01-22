from django.urls import path, include
from rest_framework import routers

from api.views import (
    TitleViewSet, GenreViewSet, CategoryViewSet,
    CommentViewSet, ReviewViewSet,
    UserSignupViewset, UserViewset, APIGetToken
)

router_api_v1 = routers.DefaultRouter()

router_api_v1.register('auth/signup', UserSignupViewset)
router_api_v1.register('users', UserViewset)
router_api_v1.register('titles', TitleViewSet, basename='titles')
router_api_v1.register('genres', GenreViewSet, basename='genres')
router_api_v1.register('categories', CategoryViewSet, basename='categories')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_api_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/token/',
         APIGetToken.as_view(),
         name='sliding_toket_obtain'),
]
