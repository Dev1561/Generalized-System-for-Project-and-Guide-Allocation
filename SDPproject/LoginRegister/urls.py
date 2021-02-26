from django.urls import path
from . import views
from EventGeneration import views as event_views
from ProjectAllocation import views as pa_views

urlpatterns = [
    path('login', views.Login),
    path('register', views.Register),
    path('logout', views.logout_user),
    path('my_assignments', views.show_my_events),
    path('my_assignment/<int:pk>', event_views.participants),
    path('my_assignment/<int:pk>/create_team', pa_views.CreateTeam),
    path('my_assignment/<int:pk>/own_definition', pa_views.own_project),
    path('', views.homepage),
    path('faculty_login', views.faculty_login),
    path('faculty_register', views.faculty_register),
]