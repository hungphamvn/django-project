from ..serializers.auth_serializers import LoginSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings


class LoginAPIView(APIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def post(self, request, format="json"):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, username=serializer.validated_data['username'])
            if not user.check_password(serializer.validated_data['password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            payload = api_settings.JWT_PAYLOAD_HANDLER(user)
            token = api_settings.JWT_ENCODE_HANDLER(payload)

            return Response(data={'token': token})

        except User.DoesNotExist as e:
            return Response(e, status=status.HTTP_401_UNAUTHORIZED)
