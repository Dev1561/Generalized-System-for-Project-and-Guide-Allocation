from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import logout

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
            return redirect('/assignments')
        else:
            messages.info(request, "Username or password incorrect!!")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

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
            return redirect('/assignments')
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
