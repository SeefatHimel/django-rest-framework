from .serializers import UserSerializer

from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print("<><><><><>>>",user, token)
        # Add custom claims
        token["name"] = user.username
        
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ListUsers(APIView):
    def get(self, request, format=None):
        
        users = User.objects.all()
        print(">>>", users, users[0])
        return Response("ok")


class RegisterAPI(APIView):
    def post(self, request,*args,**kwargs):
        print(">>>", request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = None

        # Check if username is an email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # If user is not found by email, try to authenticate with username
        if not user:
            user = authenticate(username=username, password=password)

        if user is not None:
            # Generate token
            serializer = MyTokenObtainPairSerializer()
             # Serialize user information
            user_serializer = UserSerializer(user)

            token = serializer.get_token(user)
            # Return token and user information
            response_data = {
                'access_token': str(token.access_token),
                # 'refresh_token': str(token.refresh),
                'user': user_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)