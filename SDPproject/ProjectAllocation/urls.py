from django.urls import path
from . import views

urlpatterns = [
    path('create_team', views.CreateTeam),
    path('validate_team', views.validate_team),
    path('team_created', views.team_created),
    path('allocate_project', views.allocate_project),
]