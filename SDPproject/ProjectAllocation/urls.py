from django.urls import path
from . import views

urlpatterns = [
    path('create_team', views.CreateTeam),
    path('validate_team', views.validate_team),
    path('team_created', views.team_created),
    path('team_list', views.team_list),
    path('own_project', views.own_project),
    path('allocated_projects', views.allocated_projects),
]