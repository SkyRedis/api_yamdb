from django.urls import path, include, re_path
from rest_framework import routers

from api.views import UserSignupViewset, UserViewset
from rest_framework_simplejwt.views import TokenObtainSlidingView


router_api_v1 = routers.DefaultRouter()

router_api_v1.register(r'v1/auth/signup', UserSignupViewset)
router_api_v1.register(r'v1/users', UserViewset)

urlpatterns = [
    re_path('', include(router_api_v1.urls)),
    path('v1/auth/token/',
         TokenObtainSlidingView.as_view(),
         name='token_obtain'),
]
