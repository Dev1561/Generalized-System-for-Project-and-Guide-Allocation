from django.urls import path
from . import views
from EventGeneration import views as event_views

urlpatterns = [
    path('login', views.Login),
    path('register', views.Register),
    path('logout', views.logout_user),
    path('events', event_views.Students),
    path('', views.homepage),
]