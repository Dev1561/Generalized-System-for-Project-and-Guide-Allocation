from django.urls import path
from . import views

urlpatterns = [
    path('events', views.Students),
    path('faculty', views.Faculties),
    path('create_event', views.create_event),
]