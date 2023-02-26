from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest
from users.token_service import TokenService


class RegistrationAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': "Успешная регистрация", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = TokenService.generate_token(serializer.data["id"])
            return Response({"user": serializer.data, "token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
