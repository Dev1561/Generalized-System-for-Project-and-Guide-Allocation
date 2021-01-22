from django.urls import path
from . import views

urlpatterns = [
    path('events', views.Students),
    path('create_event', views.create_event),
    path('faculty', views.Faculty)
]