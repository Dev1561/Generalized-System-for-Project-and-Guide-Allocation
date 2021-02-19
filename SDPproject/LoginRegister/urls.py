from django.urls import path
from . import views
from EventGeneration import views as event_views

urlpatterns = [
    path('login', views.Login),
    path('register', views.Register),
    path('logout', views.logout_user),
    path('assignments', event_views.Students),
    path('', views.homepage),
    path('faculty_login', views.faculty_login),
    path('faculty_register', views.faculty_register),
]