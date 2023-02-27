from users.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from django.http import HttpRequest
from users.token_service import TokenService
from users.user_service import UserService
from users.models import User
from users.serializers import UserSerializer
import uuid


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


class ManageUserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def block(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        UserService.block(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def unblock(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        UserService.unblock(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def search(self, request: HttpRequest) -> Response:
        users = UserService.search(request.GET)
        return Response({"users": users}, status=status.HTTP_200_OK)
