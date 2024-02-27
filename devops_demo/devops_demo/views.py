from django.contrib.auth.models import User
from devops_demo.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
