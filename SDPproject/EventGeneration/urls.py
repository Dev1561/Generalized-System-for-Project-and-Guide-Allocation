from django.urls import path
from . import views

urlpatterns = [
    path('assignments', views.ListAssignments),
    path('assignment/<int:pk>', views.participants),
    path('faculties', views.Faculties),
    path('students', views.Students),
    path('create_project_assignment', views.create_project_assignment),
    
]