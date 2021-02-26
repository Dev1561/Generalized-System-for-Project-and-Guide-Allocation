from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    
    def is_faculty(self):
        self.is_student = False
        
    def get_first_name(self):
        return self.get_short_name()
    
    def get_last_name(self):
        name = str(self.get_full_name())
        last_name = name.split()[1]
        return last_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.IntegerField()
    cpi=models.CharField(max_length=4)
    in_team = models.BooleanField(default=False)
    
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    designation = models.TextField(max_length=50)
    available = models.BooleanField(default=True)
    
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    faculty_user = User.objects.get(username = self.user)
    #    faculty_user.is_faculty()
    
class Event(models.Model):
    Title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    event_head = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    
    def validate_date(self):
        if self.start_date == "" or self.end_date == "":
            return False
        elif date.fromisoformat(self.start_date) < date.today() or date.fromisoformat(self.end_date) < date.fromisoformat(self.start_date):
            return False
        else:
            return True

    
class Mapping(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)