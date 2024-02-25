from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FamilyManager(models.Manager):
    pass


# Create your models here.


class FamilyUser(models.Model):
    id = models.AutoField(primary_key=True)
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"
    role_options = (
        ("OWNER", "Owner"),
        ("EDITOR", "Editor"),
        ("VIEWER", "Viewer"),
    )
    role = models.CharField(max_length=8, choices=role_options, default=None)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="family_users"
    )
    family = models.ForeignKey("Family", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("family", "user"),)


class Family(models.Model):

    name = models.CharField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(
        User, blank=False, through=FamilyUser, related_name="families"
    )

    objects = FamilyManager()


class FamilyMember(models.Model):
    name = models.CharField(max_length=50)
    img_link = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    MALE = ("MALE",)
    FEMALE = ("FEMALE",)
    gender_options = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )
    gender = models.CharField(max_length=8, choices=gender_options, default=MALE)
    children = models.ManyToManyField("FamilyMember", blank=True)
    spouse = models.ForeignKey(
        "FamilyMember",
        related_name="_spouse",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    father = models.ForeignKey(
        "FamilyMember",
        related_name="children_father",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    mother = models.ForeignKey(
        "FamilyMember",
        related_name="children_mother",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(max_length=15)
