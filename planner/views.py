from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TrainingSession
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View


# -------------------------
# Public Pages
# -------------------------

def home(request):
    sessions = TrainingSession.objects.order_by('date')
    return render(request, 'planner/home.html', {'sessions': sessions})


def about(request):
    sessions = TrainingSession.objects.order_by('date')
    return render(request, 'planner/about.html', {'sessions': sessions})


def contact(request):
    return render(request, 'planner/contact.html')


def coaching(request):
    return render(request, 'planner/coaching.html')


def pricing(request):
    return render(request, 'planner/pricing.html')


def services(request):
    return render(request, 'planner/services.html')


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


# -------------------------
# Training Sessions
# -------------------------

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


def session_complete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.completed = True
    session.save()
    return redirect('planner:session_detail', pk=pk)

# User Registration

class RegisterView(View):
    template_name = 'planner/register.html'   

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('planner:home')  # Redirect to home
        return render(request, self.template_name, {'form': form})

