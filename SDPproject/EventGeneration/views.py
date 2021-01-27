from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Event, User, Mapping
import csv, io

# Create your views here.

def Students(request):
    # spu = User.objects.get(username="jay")
    # spu.is_student = False
    # spu.save(update_fields=['is_student'])
    event_data = Event.objects.all()
    return render(request, 'show_events.html', {'event_data': event_data})

# temp view
def Faculty(request):
    event_data = Event.objects.all()
    return render(request, 'show_events.html', {'event_data':event_data})

def home(request):
    return render(request, 'base.html')

def create_event(request):
    if request.method == 'POST':
        event = Event()
        event.Title = request.POST['event_title']
        event.department = request.POST['department']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        csv_file = request.FILES['csv_file']
        if event.Title == '' or event.department == '' or event.start_date == "" or event.end_date == "":
            messages.info(request, 'all fields are mandatory')
            return redirect('/create_event')
        elif not event.validate_date():
            messages.info(request, 'Invalid date')
            return redirect('/create_event')
        else:
            event.save()
            data = csv_file.read().decode('UTF-8')
            string_data = io.StringIO(data)
            next(string_data)
            for row in csv.reader(string_data):
                user = User.objects.get(username = row[1])
                Mapping.objects.create(event_id = event,user_id = user)
                print(row)
            return redirect('/events')
    else:
        return render(request, 'create_event.html')
