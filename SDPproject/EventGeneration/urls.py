from django.urls import path
from . import views

urlpatterns = [
    path('assignments', views.Students),
    path('faculty', views.Faculties),
    path('create_project_assignment', views.create_project_assignment),
]