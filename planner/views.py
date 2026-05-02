from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TrainingSession
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.views import View
from django.utils import timezone
from django.contrib import messages


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

def free_plan(request):
    return render(request, "pricing/free_plan.html")

def pro_plan(request):
    return render(request, "pricing/pro_plan.html")

def elite_plan(request):
    return render(request, "pricing/elite_plan.html")


def session_detail(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    return render(request, 'planner/session_detail.html', {'session': session})

def session_create(request):
    if request.method == "POST":
        session = TrainingSession.objects.create(
            title="New Training Session",
            date=timezone.now().date(),
            duration=60,
            notes="Auto-created from Coaching page"
        )
        return redirect("planner:session_detail", session.id)

    return render(request, "planner/session_form.html")

def session_complete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.completed = True
    session.save()
    return redirect('planner:session_detail', pk=pk)


class RegisterView(View):
    template_name = 'planner/register.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome aboard, {user.username}! Your account is ready.")
            return redirect('planner:home')

        return render(request, self.template_name, {'form': form})


def team_dashboard(request):
    return render(request, 'services2/team_dashboard.html')

def training_builder(request):
    return render(request, 'services2/training_builder.html')

def sessions_builder(request):
    return render(request, 'services/sessions_builder.html')

def sessions_builder(request):
    return render(request, 'services2/sessions_builder.html')