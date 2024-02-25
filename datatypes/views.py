from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import FamilyListSerializer, FamilyForm, FamilyUserSerializer
from .models import FamilyUser

from base.serializers import UserSerializer


# Create your views here.
User = get_user_model()


class Families(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            families = user.families.all()
            serializer = FamilyListSerializer(families, many=True)

            return Response(serializer.data)
        except BadRequest:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FamilyUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, familyId):
        try:
            newUserId = request.data.get("id")
            newUserRole = request.data.get("role")

            family_user_serializer = FamilyUserSerializer(
                data={"user": newUserId, "family": familyId, "role": newUserRole}
            )
            if family_user_serializer.is_valid():
                family_user_serializer.save()
                families = request.user.families.get(pk=familyId)
                serialised_families = FamilyListSerializer(families)
                return Response(serialised_families.data)
            print(family_user_serializer.errors)
            return Response(
                family_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except BadRequest:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, familyId):
        try:
            oldUserId = request.data.get("id")
            newRole = request.data.get("role")
            familyUser = FamilyUser.objects.get(family_id=familyId, user_id=oldUserId)
            family_user_serializer = FamilyUserSerializer(
                familyUser, data={"role": newRole}, partial=True
            )
            if family_user_serializer.is_valid():
                family_user_serializer.save()
                return Response(family_user_serializer.data)
            print(family_user_serializer.errors)
            return Response(
                family_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except BadRequest:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, familyId):
        try:
            oldUserId = request.data.get("id")
            familyUser = FamilyUser.objects.get(family_id=familyId, user_id=oldUserId)
            familyUser.delete()
            return Response("User removed")
        except BadRequest:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FamilyUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class Family(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            form = FamilyForm(request.data)

            if form.is_valid():
                # Create a family instance but don't save it yet
                family = form.save(commit=False)

                # Save the family
                family.save()

                # Create a FamilyUser instance for the logged-in user as OWNER
                family_user = FamilyUser(
                    user=request.user, family=family, role=FamilyUser.OWNER
                )

                family_user.save()
                serializer = FamilyListSerializer(family)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)
        except BadRequest:
            return Response(status=status.HTTP_400_BAD_REQUEST)
