from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student, Event, User

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
    return render(request, 'show_events.html', {'event_data': event_data})

def create_event(request):
    if request.method == 'POST':
        event = Event()
        event.Title = request.POST['event_title']
        event.department = request.POST['department']
        event.start_date = request.POST['start_date']
        event.end_date = request.POST['end_date']
        if event.Title == '' or event.department == '' or event.start_date == "" or event.end_date == "":
            messages.info(request, 'all fields are mandatory')
            print(event.start_date)
            return redirect('/create_event')
        elif not event.validate_date():
            messages.info(request, 'Invalid date')
            return redirect('/create_event')
        else:
            event.save()
            print(type(event.start_date))
            return redirect('/events')
    else:
        return render(request, 'create_event.html')
