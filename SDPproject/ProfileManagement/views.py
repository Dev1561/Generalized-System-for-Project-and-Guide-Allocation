from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from EventGeneration import models as event_models
# Create your views here.

def profile_management(request):
    #user = User.objects.get()
    if(request.user.is_authenticated):
        if(request.user.is_student == True):
            print(request.user.is_authenticated)
            user_data = event_models.User.objects.get(username=request.user.username)
            student_data = event_models.Student.objects.get(user=user_data)
            return render(request, 'profile.html', {'student_data' : student_data})
        elif(request.user.is_student == False):
            print(request.user.is_authenticated)
            usr_data = event_models.User.objects.get(username=request.user.username)
            faculty_data = event_models.Faculty.objects.get(user=usr_data)
            return render(request, 'profile.html', {'faculty_data':faculty_data})

def profile_updated(request):
    if(request.user.is_student == True):
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
                messages.info(request, "User record not found in the database!!!")
                return redirect('/edit_profile')
            return redirect('/profile')

    elif(request.user.is_student == False):
        fac_username = request.POST['username']
        fac_first_name = request.POST['fname']
        fac_last_name = request.POST['lname']
        fac_email = request.POST['email']
        designation = request.POST['designation']
        available = request.POST['available']

        if(fac_username == ''):
            messages.info(request, "Username must not be null...")
            return redirect('/edit_profile')
        else:
            fac_user = event_models.User.objects.get(username=fac_username)
            faculty = event_models.Faculty.objects.get(user=fac_user)
            if(fac_user is not None):
                fac_user.username = fac_username
                fac_user.first_name = fac_first_name
                fac_user.last_name = fac_last_name
                fac_user.email = fac_email
                fac_user.save()

                if(faculty is not None):
                    faculty.user = fac_user
                    faculty.designation = designation
                    faculty.available = available
                    faculty.save()
                else:
                    messages.info(request, "Faculty record not found in database!!!")
                    return redirect('/edit_profile')
            else:
                messages.info(request, "User record not found in the database!!")
                return redirect('/edit_profile')
            return redirect('/profile')


def edit_profile(request):
    print(request.user)
    if request.user.is_student:
        user = event_models.Student.objects.get(user = request.user)
    elif not request.user.is_student:
        user = event_models.Faculty.objects.get(user = request.user)
    return render(request, 'edit_profile.html', {'loggedin_user':user})
