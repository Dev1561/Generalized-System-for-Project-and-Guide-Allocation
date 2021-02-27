from django.contrib import admin
from .models import Project, Team, Allocated_Project, Guide_Pref

# Register your models here.
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Allocated_Project)
admin.site.register(Guide_Pref)