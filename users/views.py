from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.http import request

class RegistrationAPIView(APIView):
    def post(self, request: request) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Успешная регистрация", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request: request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
