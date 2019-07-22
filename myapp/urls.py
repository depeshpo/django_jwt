from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from . import views


router = DefaultRouter()
router.register('api/users', views.UserViewSet, base_name='user')
router.register('api/profile', views.ProfileViewSet, base_name='profile')


urlpatterns = [
    path('', include(router.urls)),
    # path('api/auth/token', obtain_jwt_token)
]
