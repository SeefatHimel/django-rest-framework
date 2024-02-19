from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self,  email, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have a email")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email) if email else email,
            first_name = first_name,
            last_name = last_name
        )
        user_obj.set_password(password) # change user password
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,  email, first_name=None, last_name=None, password=None):
        user = self.create_user(
                email,
                first_name = first_name,
                last_name = last_name,
                password = password,
                is_staff = True
        )
        return user

    def create_superuser(self,  email, first_name=None, last_name=None, password=None):
        user = self.create_user(
                email,
                first_name = first_name,
                last_name = last_name,
                password = password,
                is_staff = True,
                is_admin = True
        )
        return user

class User(AbstractBaseUser): 
    first_name      = models.CharField(max_length=150, blank=True, null=True)
    username        = models.CharField(max_length=150, blank=True, null=True)
    last_name       = models.CharField(max_length=150, blank=True, null=True)
    email           = models.EmailField(max_length=255,unique=True, blank=False)
    is_active       = models.BooleanField(default=True) # can login 
    is_staff        = models.BooleanField(default=False) # staff user non superuser
    is_admin        = models.BooleanField(default=False) # superuser 
    timestamp       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['first_name', 'last_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
