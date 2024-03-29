import uuid

from django.http import HttpRequest
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsAdmin
from users.serializers import RegistrationSerializer, LoginSerializer
from users.serializers import UserSerializer
from users.token_service import TokenService
from users.user_service import UserService


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


class ManageUserViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'title')

    def get_permissions(self) -> BasePermission:
        permissions = {
            'list': [IsAuthenticated],
            'block': [IsAdmin],
            'unblock': [IsAdmin],
            'change_role': [IsAdmin]
        }
        return [permission() for permission in permissions.get(self.action, IsAuthenticated)]

    @action(detail=True, methods=["PATCH"])
    def block(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        UserService.block(self.get_object().pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def unblock(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        UserService.unblock(self.get_object().pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'change-role')
    def change_role(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        new_role = request.data.get("role", None)
        if new_role:
            UserService.change_role(self.get_object().pk, request.data.get("role", None))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

