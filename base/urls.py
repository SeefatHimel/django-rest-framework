from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    MyTokenObtainPairView,
    ListUsers,
    RegisterAPI,
    LoginAPI,
    UserManagement,
)

urlpatterns = [
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users", ListUsers.as_view(), name="users"),
    path("register", RegisterAPI.as_view(), name="register"),
    path("login", LoginAPI.as_view(), name="login"),
    path(
        "userManagement/<int:userId>", UserManagement.as_view(), name="UserManagement"
    ),
]
