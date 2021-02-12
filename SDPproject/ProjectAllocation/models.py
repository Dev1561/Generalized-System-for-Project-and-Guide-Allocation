from django.db import models
from EventGeneration import models as event_models

# Create your models here.

class Project(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    guide = models.ForeignKey(event_models.Faculty, on_delete=models.CASCADE, null=True)
    own_def = models.BooleanField(default=False)

class Team(models.Model):
    member1 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, related_name='member_1')
    member2 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, related_name='member_2')
    member3 = models.ForeignKey(event_models.Student, on_delete=models.CASCADE, default=None, related_name='member_3', null=True)
    preference1 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_1')    
    preference2 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_2') 
    preference3 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_3') 
    preference4 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_4') 
    preference5 = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pref_5') 