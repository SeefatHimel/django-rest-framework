from .models import Family, FamilyUser, FamilyMember
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers


class FamilyListSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "name", "created_at", "updated_at"]


class FamilyMemberParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FamilyMember
        fields = "__all__"


class FamilyMemberSerializer(serializers.ModelSerializer):
    mother = FamilyMemberParentSerializer()
    father = FamilyMemberParentSerializer()

    class Meta:
        model = FamilyMember
        fields = [
            "id",
            "name",
            "img_link",
            "phone",
            "gender",
            "spouse",
            "father",
            "mother",
            "children",
        ]

    def __init__(self, *args, **kwargs):
        # Recursive argument to handle self-referential relationships
        recursive = kwargs.pop("recursive", False)
        super(FamilyMemberSerializer, self).__init__(*args, **kwargs)
        if recursive:
            # Exclude 'spouse' field to prevent infinite recursion
            self.fields.pop("spouse", None)
        else:
            # Include 'spouse' field with recursive serializer
            self.fields["spouse"] = FamilyMemberSerializer(recursive=True)


class FamilyMemberUpdateSerializer(serializers.ModelSerializer):
    # spouse = FamilyMemberSerializer()

    class Meta:
        model = FamilyMember
        fields = [
            "id",
            "name",
            "img_link",
            "phone",
            "gender",
            "spouse",
            "father",
            "mother",
            "children",
        ]
        extra_kwargs = {"children": {"read_only": True}}


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
    members = FamilyMemberSerializer("members", many=True)

    class Meta:
        model = Family
        fields = ["id", "name", "created_at", "updated_at", "users", "members"]


from django import forms


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ["name"]
