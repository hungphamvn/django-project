from rest_framework import serializers
from django.contrib.auth.models import User


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = User
        fields = ('username', 'password')
