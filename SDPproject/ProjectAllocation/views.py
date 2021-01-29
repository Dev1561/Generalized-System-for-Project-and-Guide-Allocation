from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import AbstractUser
from .models import Project, Team
from EventGeneration import models as event_models

# Create your views here.

def CreateTeam(request):
    projects = Project.objects.all()
    return render(request, 'create_team.html', {'projects':projects})

def validate_team(request):
    members = request.POST['members']
    pref1 = request.POST['project1']
    pref2 = request.POST['project2']
    pref3 = request.POST['project3']
    pref4 = request.POST['project4']
    pref5 = request.POST['project5']
    highest_cpi = request.POST['high_cpi']

    choice1 = Project.objects.get(title=pref1)
    choice2 = Project.objects.get(title=pref2)
    choice3 = Project.objects.get(title=pref3)
    choice4 = Project.objects.get(title=pref4)
    choice5 = Project.objects.get(title=pref5)

    team_members = members.split(",")
    user1 = event_models.User.objects.get(username=team_members[0])
    user2 = event_models.User.objects.get(username=team_members[1])

    print(user1)
    print(user2)
    mem1 = event_models.Student.objects.get(user=user1)
    mem2 = event_models.Student.objects.get(user=user2)

    print(float(mem1.cpi) - float(mem2.cpi))
    print(mem2.cpi)
    if( float(mem1.cpi) - float(mem2.cpi) > 0.5 ):
        messages.info("Team cannot be created")
        return redirect('/create_team')
    else:
        team = Team()
        team.team_members = members
        team.preference1 = choice1
        team.preference2 = choice2
        team.preference3 = choice3
        team.preference4 = choice4
        team.preference5 = choice5
        team.highest_cpi = highest_cpi
        team.save()
        print("Team Created")
        return redirect('/team_created')

    return render(request, 'base.html')

def team_created(request):
    # team_data = Team.objects.get()
    return render(request, 'team_created.html')