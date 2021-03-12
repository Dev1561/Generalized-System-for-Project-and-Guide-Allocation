from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import AbstractUser
#from hungarian_algorithm import algorithm
from .models import Project, Team, Allocated_Project, Guide_Pref
from ProjectAllocation import allocate
from EventGeneration import models as event_models

# Create your views here.

def CreateTeam(request,pk):
    curr_event = event_models.Event.objects.get(pk=pk)
    teams = Team.objects.filter(event=curr_event)
    curr_user = event_models.User.objects.get(username=request.user)
    stu = event_models.Student.objects.get(user=curr_user)
    allocated_list = list(Allocated_Project.objects.filter(event_id=curr_event))
    my_team = None
    allocated_project = None
    if allocated_list:
        print(allocated_list)
    Flag = False
    for team in teams:
        if team.member1 == stu or team.member2 == stu or team.member3 == stu:
            Flag = True
            my_team = team
            break
    if Flag == True:
        for allocation in allocated_list:
            if allocation.team_id == my_team and allocation.event_id == my_team.event:
                allocated_project = allocation
        return render(request, 'my_team.html', {'team':my_team, 'event':curr_event, 'allocation':allocated_project})
    else:
        mappings = event_models.Mapping.objects.filter(event_id=curr_event)
        facs = []
        for mapping in mappings:
            user = event_models.User.objects.get(username=mapping.user_id)
            if not user.is_student:
                faculty = event_models.Faculty.objects.get(user=user)
                facs.append(faculty)
        projects = []
        for fac in facs:
            ps = list(Project.objects.filter(guide=fac))
            for p in ps:
                projects.append(p)
        my_projects = list(Project.objects.filter(owner=curr_user))
        for proj in my_projects:
            projects.append(proj)
        return render(request, 'create_team.html', {'projects':projects,'flag':Flag, 'event':curr_event})

def projects(request,pk):
    curr_event = event_models.Event.objects.get(pk=pk)
    mappings = event_models.Mapping.objects.filter(event_id=curr_event)
    projects = []
    for mapping in list(mappings):
        if not mapping.user_id.is_student:
            fac = event_models.Faculty.objects.get(user=mapping.user_id)
            p_list = Project.objects.filter(guide=fac)
            for p in p_list:
                if p.own_def == False:
                    projects.append(p)
    return render(request, 'projects_list.html', {'projects':projects, 'event':curr_event})

def validate_team(request,pk):
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
            if(Team.objects.filter(member1=mem1).exists() or Team.objects.filter(member2=mem2).exists() or Team.objects.filter(member3=mem3).exists()):
                messages.info(request, "Member already part of another team")
                return
            else:
                max_cpi = max(mem1.cpi, mem2.cpi, mem3.cpi)
                team = Team()
                curr_event = event_models.Event.objects.get(pk=pk)
                team.event = curr_event
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
            if(Team.objects.filter(member1=mem1).exists() or Team.objects.filter(member2=mem2).exists()):
                messages.info(request, "Member already part of another team")
                return
            else:
                max_cpi = max(mem1.cpi, mem2.cpi)
                team = Team()
                curr_event = event_models.Event.objects.get(pk=pk)
                team.event = curr_event
                team.member1 = mem1
                team.member2 = mem2
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

def team_list(request,pk):
    event = event_models.Event.objects.get(pk=pk)
    is_head = False
    if event.event_head.user.username == str(request.user):
        is_head = True
    team_data = Team.objects.filter(event=event)
    return render(request, 'team_list.html', {'team_data':team_data, 'is_head':is_head, 'pk':pk} )

def own_project(request,pk):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['description']
        guide_1 = request.POST['guide_1']
        guide_2 = request.POST['guide_2']
        guide_3 = request.POST['guide_3']
        print(title)
        # project = Project.objects.get(title=title)
        if(title == '' or description == '' or guide_1 == '' or guide_2 == '' or guide_3 == ''):
            messages.info(request, 'all fields are compulsory')
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
                current_user = event_models.User.objects.get(username=request.user)
                current_stu = event_models.Student.objects.get(user=current_user)
                project.owner = current_user
                project.save()
                
                guide_pref = Guide_Pref()
                guide_pref.student = current_stu
                guide_pref.project = project
                user1 = event_models.User.objects.get(username=guide_1)
                guide1 = event_models.Faculty.objects.get(user=user1)
                guide_pref.guide_1 = guide1
                user2 = event_models.User.objects.get(username=guide_2)
                guide2 = event_models.Faculty.objects.get(user=user2)
                guide_pref.guide_2 = guide2
                user3 = event_models.User.objects.get(username=guide_3)
                guide3 = event_models.Faculty.objects.get(user=user3)
                guide_pref.guide_3 = guide3
                guide_pref.save()
                # projects = Project.objects.all()
                #faculties = event_models.Faculty.objects.all()
                return redirect("/my_assignments")
    else:
        event = event_models.Event.objects.get(pk=pk)
        teams = Team.objects.filter(event=event)
        curr_user = event_models.User.objects.get(username=request.user)
        stu = event_models.Student.objects.get(user=curr_user)
        Flag = False
        for team in teams:
            if team.member1 == stu or team.member2 == stu or team.member3 == stu:
                Flag = True
                break
        if Flag == True:
            messages.info(request, "you cannot add own project after team creation")
            return redirect("teams", pk=event.id)
        else:
            mappings = event_models.Mapping.objects.filter(event_id=event)
            faculties = []
            for mapping in mappings:
                print(type(mapping.user_id))
                if not mapping.user_id.is_student:
                    faculties.append(mapping.user_id.username)
            return render(request, 'add_own_project.html', {'faculties':faculties, 'event':event})


def allocated_projects(request,pk):
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
    print(allocate.allocate_project(test_dictionary), "\n")

    print("\n",  team_dictionary, "\n")
    allocated = allocate.allocate_project(team_dictionary)

    for project in allocated:
        print("\n", project)
        if ( Allocated_Project.objects.filter(event_id=pk).exists() ) :
            return HttpResponse("Project Allocation already done for this event..!")

        allc_proj = Allocated_Project()
        curr_event = event_models.Event.objects.get(pk=pk)
        allc_proj.event_id = curr_event
        allc_proj.team_id = Team.objects.get(pk=project[0])
        allc_proj.project = Project.objects.get(title=project[1])
        allc_proj.save()

    allocated_data = Allocated_Project.objects.all()
    print(allocated_data)
    return render(request, 'allocated_project.html', {'allocated_data':allocated_data})

def guide_requests(request):
    prefernces = Guide_Pref.objects.all()
    teams = Team.objects.all()
    user = event_models.User.objects.get(username=request.user)
    current_fac = event_models.Faculty.objects.get(user=user)
    req = []
    if request.method == "GET":
        for pref in prefernces:
            if pref.guide_1 == current_fac or pref.guide_2 == current_fac or pref.guide_3 == current_fac:
                l = []
                l.append(pref)
                stu = pref.student
                for team in teams:
                    if team.member1 == stu or team.member2 == stu or team.member3 == stu:
                        l.append(team)
                req.append(l)
                
        if len(req) == 0:
            messages.info(request, 'no pending guide requests for you.')
            return redirect("/my_assignments")
        else:
            return render(request, 'requests.html', {'requests':req})
        
def process_request(request,pk):
    guide_pref = Guide_Pref.objects.get(pk=pk)
    if request.method == "POST":
        project = guide_pref.project
        final_user = event_models.User.objects.get(username=request.user)
        final_guide = event_models.Faculty.objects.get(user=final_user)
        project.guide = final_guide
        project.save(update_fields=['guide'])
        guide_pref.delete()
        return redirect('/guide_requests')
    else:
        return render(request, 'request.html', {'guide_pref':guide_pref})

def add_project(request):
    if(request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['description']

        if(title == '' or description == ''):
            messages.info(request, "All fields are compulsory...")
            return render(request, 'add_project.html')
        else:
            if(Project.objects.filter(title=title).exists()):
                messages.info(request, "Project with same title already exists...")
                return render(request, 'add_project.html')
            else:
                user = event_models.User.objects.get(username=request.user)
                guide = event_models.Faculty.objects.get(user=user)
                project = Project()
                project.title = title
                project.description = description
                project.guide = guide
                project.owner = user
                project.save()
                return redirect("/my_assignments")
    else:
        return render(request, 'add_project.html')  


def allocated_data(request):
    user = event_models.Mapping.objects.get(user_id=request.user)
    allocated_data = Allocated_Project.objects.filter(event_id=user.event_id)
    print(allocated_data)
    # return HttpResponse(allocated_data.team_id.member1.user.username)
    return render(request, 'allocated_project.html', {'allocated_data':allocated_data})