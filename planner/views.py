from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TrainingSession

def home(request):
    sessions = TrainingSession.objects.order_by('date')
    return render(request, 'planner/home.html', {'sessions': sessions})


def session_detail(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    return render(request, 'planner/session_detail.html', {'session': session})


def session_create(request):
    if request.method == 'POST':
        TrainingSession.objects.create(
            title=request.POST['title'],
            date=request.POST['date'],
            duration=request.POST['duration'],
            notes=request.POST.get('notes', '')
        )
        return redirect('planner:home')

    return render(request, 'planner/session_form.html')

def contact(request):
    return render(request, 'planner/contact.html')

def coaching(request):
    return render(request, 'planner/coaching.html')

def pricing(request):
    return render(request, 'planner/pricing.html')

def features(request):
    return render(request, 'planner/features.html')

def team_management(request):
    return render(request, 'planner/team_management.html')

def season_planner(request):
    return render(request, 'planner/season_planner.html')

def training_planner(request):
    return render(request, 'planner/training_planner.html')

def sessions_2d3d(request):
    return render(request, 'planner/sessions_2d3d.html')

def drill_library(request):
    return render(request, 'planner/drill_library.html')

def session_complete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.completed = True
    session.save()
    return redirect('planner:session_detail', pk=pk)

def about(request):
    return render(request, 'planner/about.html')
