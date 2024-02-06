from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("products", views.products),
    path("products/<int:id>", views.product),
]

urlpatterns = format_suffix_patterns(urlpatterns)
