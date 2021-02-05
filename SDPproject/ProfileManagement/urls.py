from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile_management),
    path('edit_profile', views.edit_profile),
    path('profile_updated', views.profile_updated),
]