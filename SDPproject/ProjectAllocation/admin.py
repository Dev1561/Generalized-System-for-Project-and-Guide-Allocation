from django.contrib import admin
from .models import Project, Team, Allocated_Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Allocated_Project)