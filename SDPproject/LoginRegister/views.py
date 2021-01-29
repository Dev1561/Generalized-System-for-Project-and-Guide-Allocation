from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import logout

from EventGeneration.models import User, Student
# Create your views here.

def Login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if (user is not None) :
            auth.login(request, user)
            print(user.is_authenticated)
            if(user.is_superuser):
                return redirect('adminpanel/events')
            else:
                return HttpResponse("page is yet to be designed")
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
                return redirect('/events')
    else:
        return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')

    

