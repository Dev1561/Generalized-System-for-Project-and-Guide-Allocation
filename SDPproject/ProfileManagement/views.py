from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from EventGeneration import models as event_models
# Create your views here.

def profile_management(request):
    #user = User.objects.get()
    if(request.user.is_authenticated):
        print(request.user.is_authenticated)
        user_data = event_models.User.objects.get(username=request.user.username)
        student_data = event_models.Student.objects.get(user=user_data)
        return render(request, 'profile.html', {'student_data' : student_data})

def profile_updated(request):
    username = request.POST['username']
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    roll_no = request.POST['roll_no']
    cpi = request.POST['cpi']

    if(username == ''):
        messages.info(request, "Username must not be null...")
        return redirect('/edit_profile')
    else:
        user = event_models.User.objects.get(username=username)
        student = event_models.Student.objects.get(user=user)
        if(user is not None):
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            if(student is not None):
                student.user = user
                student.roll_no = roll_no
                student.cpi = cpi
                student.save()
            else:
                messages.info(request, "Student record not found in database!!!")
                return redirect('/edit_profile')
        else:
            messages.info(request, "User record found in the database!!!")
            return redirect('/edit_profile')
        return render(request, 'profile_updated.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')