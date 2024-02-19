from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name', 'last_name','id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("🐍 File: base/serializers.py | Line: 11 | Meta: ~ validated_data",validated_data)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user