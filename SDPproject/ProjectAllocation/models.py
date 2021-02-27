from django.db import models
from EventGeneration import models as event_models

# Create your models here.

class Project(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    guide = models.ForeignKey(event_models.Faculty, on_delete=models.CASCADE, null=True)
    own_def = models.BooleanField(default=False)
    owner = models.ForeignKey(event_models.User, on_delete=models.CASCADE, default=None, null=True)

class Team(models.Model):
    event = models.ForeignKey(event_models.Event, on_delete=models.CASCADE)
    member1 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, related_name='member_1')
    member2 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, related_name='member_2')
    member3 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, default=None, related_name='member_3', null=True)
    preference1 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_1')    
    preference2 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_2') 
    preference3 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_3') 
    preference4 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_4') 
    preference5 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_5') 
    highest_cpi = models.CharField(max_length=4, null=True)
    
class Guide_Pref(models.Model):
     student = models.ForeignKey(event_models.Student, on_delete=models.CASCADE)
     project = models.ForeignKey(Project, on_delete=models.CASCADE)
     guide_1 = models.ForeignKey(event_models.Faculty, on_delete=models.CASCADE, related_name='guide_1')
     guide_2 = models.ForeignKey(event_models.Faculty, on_delete=models.CASCADE, related_name='guide_2')
     guide_3 = models.ForeignKey(event_models.Faculty, on_delete=models.CASCADE, related_name='guide_3')

class Allocated_Project(models.Model):
    event_id = models.ForeignKey(event_models.Event, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)