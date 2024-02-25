from django.urls import path
from .views import Families, Family, FamilyUserAPI, FamilyMembersAPI

urlpatterns = [
    path("list", Families.as_view(), name="Families"),
    path("create", Family.as_view(), name="Createfamily"),
    path("<int:familyId>/user", FamilyUserAPI.as_view(), name="AddFamilyuser"),
    path("<int:familyId>/member", FamilyMembersAPI.as_view(), name="AddFamilyMember"),
]
