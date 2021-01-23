from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.IntegerField()
    college_id = models.CharField(max_length=10,primary_key=True)
    cpi=models.CharField(max_length=4)
    
class Event(models.Model):
    Title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def validate_date(self):
        if self.start_date == "" or self.end_date == "":
            return False
        elif date.fromisoformat(self.start_date) < date.today() or date.fromisoformat(self.end_date) < date.fromisoformat(self.start_date):
            return False
        else:
            return True
