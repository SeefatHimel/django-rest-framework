from django.urls import path
from .views import Families, Family, FamilyMember

urlpatterns = [
    path("list", Families.as_view(), name="Families"),
    path("create", Family.as_view(), name="Createfamily"),
    path("<int:familyId>", FamilyMember.as_view(), name="AddFamilyMember"),
]
