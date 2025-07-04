from django.shortcuts import render
from rest_framework import viewsets, generics

from user.serializers import CreateUserSerializer


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer