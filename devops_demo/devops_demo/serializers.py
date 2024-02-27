from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "id", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}
