from django.urls import path
from . import views

urlpatterns = [
    path('faculty', views.Faculty),
    path('', views.home),
    path('events', views.Students),
    path('create_event', views.create_event),
]