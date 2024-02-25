from .serializers import UserSerializer

from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("<><><><><>>>", user, token)
        # Add custom claims
        token["name"] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ListUsers(APIView):
    def get(self, request, format=None):

        users = User.objects.all()
        print(">>>", users, users[0])
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        print(">>>", request.data)
        # return Response(request.data, status=status.HTTP_201_CREATED)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        authenticatedUser = None

        email = True

        # Check if username is an email
        try:
            valid = validate_email(username)
        except ValidationError:
            email = False

        # Check if the user exists
        if email:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                user = User.objects.get(username=username)
                username = user.email
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        # If user exists then we authenticate user
        try:
            authenticatedUser = authenticate(username=username, password=password)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        print(
            "🐍 File: base/views.py | Line: 78 | post ~ authenticatedUser",
            authenticatedUser,
        )
        # If user is authenticated return user and token
        if authenticatedUser is not None:
            # Generate token
            serializer = MyTokenObtainPairSerializer()
            # Serialize user information
            user_serializer = UserSerializer(authenticatedUser)

            token = serializer.get_token(authenticatedUser)
            # Return token and user information
            response_data = {
                "access_token": str(token.access_token),
                # 'refresh_token': str(token.refresh),
                "user": user_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserManagement(APIView):

    def delete(self, request, userId):
        print(
            "🐍 File: base/views.py | Line: 91 | UserManagement ~ request, user_id",
            userId,
        )

        # return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            user = User.objects.get(
                pk=userId
            )  # Assuming your User model has a primary key named 'id'
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
