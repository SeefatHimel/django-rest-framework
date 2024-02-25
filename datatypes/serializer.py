from .models import Family, FamilyUser
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers


class FamilyListSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "name", "created_at", "updated_at"]


class FamilyUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    email = serializers.CharField(
        source="user.email",
        read_only=True,
    )
    userId = serializers.IntegerField(
        source="user.id",
        read_only=True,
    )
    # families = FamilyListSerializer2(
    #     source="user.families",
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        model = FamilyUser
        fields = (
            "id",
            "userId",
            "username",
            "role",
            "email",
            # "families",
            "user",
            "family",
        )
        extra_kwargs = {"user": {"write_only": True}, "family": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    role = FamilyUserSerializer(source="family_users")

    class Meta:
        model = User
        fields = "__all__"


class FamilyListSerializer(serializers.ModelSerializer):
    users = FamilyUserSerializer(source="familyuser_set", many=True)

    class Meta:
        model = Family
        fields = ["id", "name", "created_at", "updated_at", "users"]


from django import forms


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ["name"]
