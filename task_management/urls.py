from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks", views.tasks),
    path("task/<int:id>", views.task),
]

urlpatterns = format_suffix_patterns(urlpatterns)
