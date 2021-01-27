from django.shortcuts import render, redirect
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
            print("World!!!")
            auth.login(request, user)
            return redirect('/events')
        else:
            print("Dev")
            return render(request, 'login.html')
    else:
        print("Parmar")
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
            return render(request, 'register.html')
        else:
            if User.objects.filter(username = username).exists() :
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
    
