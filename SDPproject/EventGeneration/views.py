from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Event, User, Mapping, Faculty
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

def Faculties(request):
    event_data = Event.objects.all()
    user_faculty = User.objects.get(username = "SDP")
    user_faculty.is_faculty()
    faculty = Faculty.objects.get(user = user_faculty)
    print(faculty.user)
    return render(request, 'faculty_page.html')
    #return render(request, 'show_events.html', {'event_data':event_data})
    
def Students(request):
    students_list = Student.objects.all()
    return render(request, 'student_list.html', {'students':students_list})

def create_project_assignment(request):
    if request.method == 'POST':
        event = Event()
        event.Title = request.POST['event_title']
        event.department = request.POST['department']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        csv_file = request.FILES.get('file', False)
        if event.Title == '' or event.department == '' or event.start_date == "" or event.end_date == "":
            messages.info(request, 'all fields are mandatory')
            print(event.start_date)
            return redirect('/create_event')
        elif not event.validate_date():
            messages.info(request, 'Invalid date')
            return redirect('/create_event')
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


