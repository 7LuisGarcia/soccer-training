from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import TrainingSession
from .forms import CustomUserCreationForm


def home(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/home.html", {"sessions": sessions})


def about(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/about.html", {"sessions": sessions})

def real_app_features(request):
    return render(request, "services/real_app_features.html")


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Form Message from {name}"

        body = f"""
Name: {name}
Email: {email}

Message:
{message}
"""

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        messages.success(request, "Message sent successfully!")

        return redirect("planner:contact")

    return render(request, "planner/contact.html")

def coach_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        return redirect("planner:login")

    return wrapper


@login_required
@coach_required
def create_session(request):
    return render(request, "planner/create_session.html")

def coaching(request):
    return render(request, "planner/coaching.html")


def pricing(request):
    return render(request, "planner/pricing.html")


def services(request):
    return render(request, "planner/services.html")


def planner_team_management(request):
    return render(request, "services/team_management.html")


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
        title = request.POST.get("title")
        date = request.POST.get("date")
        duration = request.POST.get("duration")
        notes = request.POST.get("notes")

        session = TrainingSession.objects.create(
            title=title,
            date=date,
            duration=duration,
            notes=notes,
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
    return render(request, "services/sessions_builder.html")


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

def sessions_builder(request):
    return render(request, "services/session_builder.html")

from django.shortcuts import render
from .models import Team

def coaching_system(request):
    teams = Team.objects.prefetch_related(
        "players",
        "seasons__weekly_goals__sessions__session_drills__drill",
        "seasons__weekly_goals__sessions__attendance",
        "seasons__weekly_goals__sessions__performances",
    )

    return render(request, "planner/coaching_system.html", {
        "teams": teams
    })

@login_required
def dashboard(request):
    return render(request, "planner/dashboard.html")


@login_required
def analytics(request):
    return render(request, "planner/analytics.html")
