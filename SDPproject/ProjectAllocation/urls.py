from django.urls import path
from . import views

urlpatterns = [
    #path('create_team', views.CreateTeam),
    path('my_assignment/<int:pk>/validate_team', views.validate_team),
    path('team_created', views.team_created),
<<<<<<< HEAD
    path('my_assignment/<int:pk>/team_list', views.team_list),
=======
    path('team_list/<int:pk>', views.team_list),
>>>>>>> 31c38185ec1f4c293ee8d09aeea96d7b0e8e8183
    path('guide_requests', views.guide_requests),
    path('guide_request/<int:pk>', views.process_request),
    path('my_assignment/<int:pk>/own_project', views.own_project),
    path('allocated_projects/<int:pk>', views.allocated_projects),
    path('add_project/<int:pk>', views.add_project),
]