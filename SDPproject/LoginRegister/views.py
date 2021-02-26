from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import logout
from EventGeneration import models as event_models

from EventGeneration.models import User, Student, Faculty
# Create your views here.

def Login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if (user is not None) :
            auth.login(request, user)
            print(user.is_authenticated)
            if user.is_superuser:
                return redirect('/assignments')
            else:
                return redirect('/my_assignments')
        else:
            messages.info(request, "Username or password incorrect!!")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def show_my_events(request):
    mappings = event_models.Mapping.objects.all()
    #print(mappings)
    my_events = []
    for mapping in mappings:
        #print(mapping.event_id)
        if mapping.user_id == request.user:
            event_obj = mapping.event_id
            event = event_models.Event.objects.get(pk=event_obj.id)
            my_events.append(event)
    print(my_events)
    return render(request, 'my_events.html', {'my_events':my_events})

# def my_event(request,pk):
#     event = Event.objects.get(pk=pk)
#     mapped_objects = Mapping.objects.all()
#     students = []
#     faculties = []
#     for obj in list(mapped_objects):
#         #print(obj.event_id)
#         print(obj.user_id)
#         if obj.event_id == event:
#             user = User.objects.get(username=obj.user_id)
#             if user.is_student:
#                 stu = Student.objects.get(user=obj.user_id)
#                 students.append(stu)
#                 #print(stu.roll_no)
#             else:
#                 fac = Faculty.objects.get(user=obj.user_id)
#                 faculties.append(fac)
        
#     return render(request, 'participants_list.html', {'students':students, 'faculties':faculties})
    
    

def Register(request):
    
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        rollno = request.POST['rollno']
        cpi = request.POST['cpi']

        if (username == '' or password == ''):
            messages.info(request, "Username or password must not be null...")
            return render(request, 'register.html')
        else:
            if User.objects.filter(username = username).exists() :
                messages.info(request, "User with username already exists...")
                return render(request, 'register.html')
            else :
                user, created = User.objects.get_or_create(username = username, email = email, first_name = fname, last_name = lname)
                user.set_password(password)
                user.save()
                student = Student()
                student.user = user
                student.roll_no = rollno
                student.cpi = cpi
                student.save()
                return redirect('/login')
    else:
        return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')

def homepage(request):
    return render(request, 'new_base.html')

def faculty_login(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if (user is not None) :
            auth.login(request, user)
            print(user.is_authenticated)
            print(user.is_student)
            return redirect('/my_assignments')
        else:
            messages.info(request, "Username or password incorrect!!")
            return render(request, 'faculty_login.html')
    else:
        return render(request, 'faculty_login.html')

def faculty_register(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        designation = request.POST['designation']
        available = request.POST['available']

        if(username == '' or password == ''):
            messages.info(request, "Username or password cannot be null!!!")
            return render(request, 'faculty_register.html')
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User already exists with given username!!!")
                return render(request, 'faculty_register.html')
            else:
                user, created = User.objects.get_or_create(username=username, email=email, first_name=fname, last_name=lname)
                user.set_password(password)
                user.is_student = False
                user.save()
                faculty = Faculty()
                faculty.user = user
                faculty.designation = designation
                faculty.available = available
                faculty.save()
                return redirect('/assignments')
    else:
        return render(request, 'faculty_register.html')
