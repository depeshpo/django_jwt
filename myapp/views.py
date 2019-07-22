from django.contrib.auth import user_logged_in
from rest_framework import status

from jwt_basic import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response

import jwt
from myapp.custom_payload_handler import custom_payload_handler
from .serializers import ProfileReadSerializer, ProfileWriteSerializer, UserSerializer
from .models import User, Profile


class Login(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.get(email=email)

            if user.check_password(password) and user.is_active:
                try:
                    payload = custom_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    user_details = {}
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    response = Response(user_details)
                    return response
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'Can not authenticate with given credentials'
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {
                'error': 'Please provide an email and password'
            }
            return Response(res)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE' \
                or self.request.method == 'PATCH':
            return ProfileWriteSerializer
        return ProfileReadSerializer
