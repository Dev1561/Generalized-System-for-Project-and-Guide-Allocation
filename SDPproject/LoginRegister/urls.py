from django.urls import path
from . import views

urlpatterns = [ 
    path('login', views.Login),
    path('register', views.Register),
    path('login/homeview', views.homeview),
    path('logout', views.logout_user),
]