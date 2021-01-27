from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Event, Mapping
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Mapping)