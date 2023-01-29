from django.urls import include, path
from rest_framework import routers

from .routers import RouterModelSlug, RouterNoPUT
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, MeView, ReviewViewSet, TitleViewSet,
                    UserSignupView, UserViewset)

router_api_v1 = routers.DefaultRouter()
router_api_v1_no_PUT = RouterNoPUT()
router_api_v1_Model_Slug = RouterModelSlug()

router_api_v1_no_PUT.register('users', UserViewset)
router_api_v1.register('titles', TitleViewSet, basename='titles')
router_api_v1_Model_Slug.register('genres', GenreViewSet, basename='genres')
router_api_v1_Model_Slug.register(
    'categories', CategoryViewSet, basename='categories')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('users/me/', MeView.as_view(), name='me'),
    path('', include(router_api_v1.urls)),
    path('', include(router_api_v1_no_PUT.urls)),
    path('', include(router_api_v1_Model_Slug.urls)),
    path('auth/signup/', UserSignupView.as_view(), name='user_register'),
    path('auth/token/',
         GetTokenView.as_view(),
         name='sliding_toket_obtain'),
]
