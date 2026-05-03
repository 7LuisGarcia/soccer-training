from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.utils import timezone

from .models import TrainingSession
from .forms import CustomUserCreationForm


def home(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/home.html", {"sessions": sessions})


def about(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/about.html", {"sessions": sessions})


def contact(request):
    return render(request, "planner/contact.html")


def coaching(request):
    return render(request, "planner/coaching.html")


def pricing(request):
    return render(request, "planner/pricing.html")


def services(request):
    return render(request, "planner/services.html")


def planner_team_management(request):
    return render(request, "planner/team_management.html")


def season_planner(request):
    return render(request, "planner/season_planner.html")


def training_planner(request):
    return render(request, "planner/training_planner.html")


def sessions_2d3d(request):
    return render(request, "planner/sessions_2d3d.html")


def drill_library(request):
    return render(request, "planner/drill_library.html")


def free_plan(request):
    return render(request, "pricing/free_plan.html")


def pro_plan(request):
    return render(request, "pricing/pro_plan.html")


def elite_plan(request):
    return render(request, "pricing/elite_plan.html")


def session_detail(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    return render(request, "planner/session_detail.html", {"session": session})


def session_create(request):
    if request.method == "POST":
        session = TrainingSession.objects.create(
            title="New Training Session",
            date=timezone.now().date(),
            duration=60,
            notes="Auto-created from Coaching page",
        )
        return redirect("planner:session_detail", pk=session.pk)

    return render(request, "planner/session_form.html")


def session_complete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.completed = True
    session.save()
    return redirect("planner:session_detail", pk=pk)


class RegisterView(View):
    template_name = "planner/register.html"

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome aboard, {user.username}! Your account is ready.",
            )
            return redirect("planner:home")

        return render(request, self.template_name, {"form": form})


def player_tracking(request):
    return render(request, "services/player_tracking.html")


def training_builder(request):
    return render(request, "services/training_builder.html")


def sessions_builder(request):
    return render(request, "services/session_builder.html")


def services_team_management(request):
    return render(request, "services/team_management.html")


def player_detail(request, id):
    return render(request, "services/player_detail.html", {"player_id": id})

def advanced_analytics(request):
    return render(request, "services/advanced_analytics.html")


def team_dashboard(request):
    return render(request, "planner/team_dashboard.html")

def drill_library(request):
    return render(request, "services/drill_library.html")

def season_planner(request):
    return render(request, "services/season_planner.html")

def training_planner(request):
    return render(request, "services/training_planner.html")

def sessions_2d3d(request):
    return render(request, "services/sessions_2d3d.html")

def player_tracking(request):
    return render(request, "services/player_tracking.html")

def player_tracking(request):
    return render(request, "services/player_tracking.html")

def advanced_analytics(request):
    return render(request, "services/advanced_analytics.html")

def planner_team_management(request):
    return render(request, "services/team_management.html")

