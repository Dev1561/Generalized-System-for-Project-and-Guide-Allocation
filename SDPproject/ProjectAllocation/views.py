from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import AbstractUser
#from hungarian_algorithm import algorithm
from .models import Project, Team, Allocated_Project
from ProjectAllocation.test import *
from EventGeneration import models as event_models

# Create your views here.

def CreateTeam(request):
    projects = Project.objects.all()
    return render(request, 'create_team.html', {'projects':projects})

def validate_team(request):
    member1 = request.POST['member1']
    member2 = request.POST['member2']
    member3 = request.POST['member3']
    pref1 = request.POST['project1']
    pref2 = request.POST['project2']
    pref3 = request.POST['project3']
    pref4 = request.POST['project4']
    pref5 = request.POST['project5']
    print(pref1)
    print(pref2)
    print(pref3)
    print(pref4)
    print(pref5)
    choice1 = Project.objects.get(title=pref1)
    choice2 = Project.objects.get(title=pref2)
    choice3 = Project.objects.get(title=pref3)
    choice4 = Project.objects.get(title=pref4)
    choice5 = Project.objects.get(title=pref5)

    user1 = event_models.User.objects.get(username=member1)
    user2 = event_models.User.objects.get(username=member2)
    user3 = None
    if(member3 == ''):
        member3 = None
    if(member3 is not None):
        user3 = event_models.User.objects.get(username=member3)
        
    mem1 = event_models.Student.objects.get(user=user1)
    mem2 = event_models.Student.objects.get(user=user2)
    mem3 = None
    if(user3 is not None):
        mem3 = event_models.Student.objects.get(user=user3)

    print(float(mem1.cpi) - float(mem2.cpi))

    if(mem3 is not None):
        if( ( float(mem1.cpi) - float(mem2.cpi) - float(mem3.cpi) ) > 0.5 ):
            messages.info(request, "Team cannot be created")
            return redirect('/create_team')
        else:
            max_cpi = max(mem1.cpi, mem2.cpi, mem3.cpi)
            team = Team()
            team.member1 = mem1
            team.member2 = mem2
            team.member3 = mem3
            team.preference1 = choice1
            team.preference2 = choice2
            team.preference3 = choice3
            team.preference4 = choice4
            team.preference5 = choice5
            team.highest_cpi = max_cpi
            team.save()
            print("Team Created")
            return redirect('/team_created')
    else:
        if( ( float(mem1.cpi) - float(mem2.cpi) ) > 0.5 ):
            messages.info(request, "Team cannot be created")
            return redirect('/create_team')
        else:
            max_cpi = max(mem1.cpi, mem2.cpi)
            team = Team()
            team.member1 = mem1
            team.member2 = mem2
            team.member3 = mem3
            team.preference1 = choice1
            team.preference2 = choice2
            team.preference3 = choice3
            team.preference4 = choice4
            team.preference5 = choice5
            team.highest_cpi = max_cpi
            team.save()
            print("Team Created")
            return redirect('/team_created')

    return render(request, 'base.html')

def team_created(request):
    # team_data = Team.objects.get()
    return render(request, 'team_created.html')

def team_list(request):
    team_data = Team.objects.all()
    return render(request, 'team_list.html', {'team_data':team_data} )

def own_project(request):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['description']
        print(title)
        # project = Project.objects.get(title=title)
        if(title == '' or description == ''):
            messages.info(request, 'Title or description must not be empty!!!')
            return redirect('/own_project')
        else:
            if( Project.objects.filter(title=title).exists() ):
                messages.info(request, "Project with given title already exists in database!!!")
                return redirect('/own_project')
            else:
                project = Project()
                project.title = title
                project.description = description
                project.own_def = True
                project.save()
                
                # projects = Project.objects.all()
                faculties = event_models.Faculty.objects.all()
                return render(request, 'project_added.html', {'faculties':faculties})
    else:
        return render(request, 'add_own_project.html')


def allocated_projects(request):
    i = 0
    team_data = Team.objects.all()
    sorted_team_data = Team.objects.order_by('-highest_cpi')
    print(sorted_team_data , "\n\n")
    team_dictionary = { }
    print("\n", len(sorted_team_data))
    for i in range (0, len(sorted_team_data)):
        mydict = { }
        j = 1
        mydict.update({ sorted_team_data[i].preference1.title : j+4 })
        mydict.update({ sorted_team_data[i].preference2.title : j+3 })
        mydict.update({ sorted_team_data[i].preference3.title : j+2 })
        mydict.update({ sorted_team_data[i].preference4.title : j+1 })
        mydict.update({ sorted_team_data[i].preference5.title : j })
        print(mydict)
        team_dictionary.update( {sorted_team_data[i].pk : mydict } )
        i = i + 1
    
    test_dictionary = {'Team1': {'Project Allocation System': 5, 'Catering Management System': 4, 'Online Car Rental System': 3, 'Doubt solving platform': 2, 'Restaurant Management System': 1}, 'Team2': {'Online Car Rental System': 5, 'Project Allocation System': 4, 'Matrimonial System': 3, 'Restaurant Management System': 2, 'Catering Management System': 1}, 'Team3': {'Project Allocation System': 5, 'Online Car Rental System': 4, 'Catering Management System': 3, 'Matrimonial System': 2, 'Doubt solving platform': 1}}
    print("\n")
    print(allocate_project(test_dictionary), "\n")

    print("\n",  team_dictionary, "\n")
    allocated = allocate_project(team_dictionary)

    for project in allocated:
        print("\n", project)
        allc_proj = Allocated_Project()
        # allc_proj.event_id = 
        allc_proj.team_id = Team.objects.get(pk=project[0])
        allc_proj.project = Project.objects.get(title=project[1])
        allc_proj.save()

    allocated_data = Allocated_Project.objects.all()
    print(allocated_data)
    return render(request, 'allocated_project.html', {'allocated_data':allocated_data})