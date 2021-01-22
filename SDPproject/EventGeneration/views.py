from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Event, User

# Create your views here.
def Students(request):
    # spu = User.objects.get(username="jay")
    # spu.is_student = False
    # spu.save(update_fields=['is_student'])
    event_data = Event.objects.all()
    return render(request, 'show_events.html', {'event_data':event_data})

def Faculty(request):
    event_data = Event.objects.all()
    return render(request, 'show_events.html', {'event_data':event_data})

def home(request):
    return render(request, 'base.html')
