from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status

from .models import User
from .permissions import AccountOwnerPermission, AdminPermission
from .serializers import ChangeActiveSerializer, LoginSerializer, UserSerializer


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListByDateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        max_users = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:max_users]


class UpdateAccountView(generics.UpdateAPIView):
    permission_classes = [AccountOwnerPermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChangeActiveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, AdminPermission]

    queryset = User.objects.all()
    serializer_class = ChangeActiveSerializer
