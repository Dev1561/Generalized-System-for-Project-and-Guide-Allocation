from django.urls import path
from . import views

urlpatterns = [
    path('students', views.Students),
    path('faculty', views.Faculty),
    path('', views.home),
]