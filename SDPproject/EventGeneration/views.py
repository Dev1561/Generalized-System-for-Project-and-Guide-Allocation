from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Event, User, Mapping, Faculty
from ProjectAllocation.models import Project, Team, Allocated_Project
import csv
import io

# Create your views here.
def ListAssignments(request):
    # spu = User.objects.get(username="jay")
    # spu.is_student = False
    # spu.save(update_fields=['is_student'])
    event_data = Event.objects.all()
    return render(request, 'show_events.html', {'event_data':event_data})

def participants(request,pk):
    event = Event.objects.get(pk=pk)
    mapped_objects = Mapping.objects.all()
    students = []
    faculties = []
    for obj in list(mapped_objects):
        #print(obj.event_id)
        print(obj.user_id)
        if obj.event_id == event:
            user = User.objects.get(username=obj.user_id)
            if user.is_student:
                stu = Student.objects.get(user=obj.user_id)
                students.append(stu)
                #print(stu.roll_no)
            else:
                fac = Faculty.objects.get(user=obj.user_id)
                faculties.append(fac)
        
    return render(request, 'participants_list.html', {'students':students, 'faculties':faculties})

def participants1(request,pk):
    event = Event.objects.get(pk=pk)
    mapped_objects = Mapping.objects.all()
    students = []
    faculties = []
    for obj in list(mapped_objects):
        #print(obj.event_id)
        print(obj.user_id)
        if obj.event_id == event:
            user = User.objects.get(username=obj.user_id)
            if user.is_student:
                stu = Student.objects.get(user=obj.user_id)
                students.append(stu)
                #print(stu.roll_no)
            else:
                fac = Faculty.objects.get(user=obj.user_id)
                faculties.append(fac)
        
    return render(request, 'participants_list1.html', {'students':students, 'faculties':faculties, 'event':event})

def Faculties(request):
    # event_data = Event.objects.all()
    # user_faculty = User.objects.get(username = "SDP")
    # user_faculty.is_faculty()
    # faculty = Faculty.objects.get(user = user_faculty)
    # print(faculty.user)
    # return render(request, 'faculty_list.html')
    #return render(request, 'show_events.html', {'event_data':event_data})
    faculties = Faculty.objects.all()
    faculty_list = list(faculties)
    faculty_list.sort(key = lambda Faculty: Faculty.user.first_name)
    return render(request, 'faculty_list.html', {'faculties':faculty_list})
    
def Students(request):
    students = Student.objects.all()
    students_list = list(students)
    students_list.sort(key = lambda Student: Student.user.first_name)
    return render(request, 'student_list.html', {'students':students_list})

def admin_team_list(request,pk):
    event = Event.objects.get(pk=pk)
    team_data = Team.objects.filter(event=event)
    return render(request, 'admin_team_list.html', {'team_data':team_data, 'event':event})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects':projects})

def project_allocation_list(request,pk):
    event = Event.objects.get(pk=pk)
    allocation_list = Allocated_Project.objects.filter(event_id=event)
    if not len(list(allocation_list)):
        messages.info(request, "project allocation is not yet done")
        if request.user.is_superuser:
            return redirect("admin_team_list", pk=event.id)
        else:
            return redirect('/my_assignments')
    else:
        return render(request, 'allocation_list.html', {'allocation_list':allocation_list, 'event':event})

def create_project_assignment(request):
    if request.method == 'POST':
        event = Event()
        event.Title = request.POST['event_title']
        event.department = request.POST['department']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        event_head = request.POST['event_head']
        user = User.objects.get(username = event_head)
        event.event_head = Faculty.objects.get(user = user)
        csv_file = request.FILES.get('file', False)
        if event.Title == '' or event.department == '' or event.start_date == "" or event.end_date == "" or event.event_head == None:
            messages.info(request, 'all fields are mandatory')
            print(event.start_date)
            return redirect('/create_project_assignment')
        elif not event.validate_date():
            messages.info(request, 'Invalid date')
            return redirect('/create_project_assignment')
        else:
            event.save()
            data = csv_file.read().decode('UTF-8')
            string = io.StringIO(data)
            next(string)
            reader = csv.reader(string)
            for row in reader:
                print(row[1])
                user = User.objects.get(username = row[1])
                Mapping.objects.create(event_id = event, user_id = user)
                #participant.event_id.add(event)
                
                #participant.user_id.add(user)
            return redirect('/assignments')
    else:
        return render(request, 'create_event.html')


