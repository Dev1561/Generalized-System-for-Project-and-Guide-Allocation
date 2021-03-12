from django.urls import path
from . import views

urlpatterns = [
    path('assignments', views.ListAssignments),
    path('assignment/<int:pk>', views.participants),
    path('assignment/<int:pk>/team_list', views.admin_team_list, name="admin_team_list"),
    path('assignment/<int:pk>/allocation_list', views.project_allocation_list),
    path('my_assignment/<int:pk>/allocation_list', views.project_allocation_list),
    path('faculties', views.Faculties),
    path('students', views.Students),
    path('projects', views.projects),
    path('create_project_assignment', views.create_project_assignment),
    
]