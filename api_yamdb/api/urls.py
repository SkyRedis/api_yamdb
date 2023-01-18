from api.views import CommentViewSet, ReviewViewSet
from django.urls import include, re_path
from rest_framework import routers

router_api_v1 = routers.DefaultRouter()

router_api_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_api_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    re_path('', include(router_api_v1.urls)),
]
