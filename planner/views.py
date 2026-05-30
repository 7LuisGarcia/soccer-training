from functools import wraps

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import TrainingSession, UserProfile, Team, Player, Attendance, PlayerPerformance


def coach_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and hasattr(request.user, "userprofile")
            and request.user.userprofile.role == "coach"
        ):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Only coaches can access this page.")
        return redirect("planner:dashboard")
    return wrapper


def home(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/home.html", {"sessions": sessions})


def about(request):
    sessions = TrainingSession.objects.order_by("date")
    return render(request, "planner/about.html", {"sessions": sessions})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = f"New Contact Form Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        send_mail(subject, body, settings.EMAIL_HOST_USER, [settings.CONTACT_EMAIL], fail_silently=False)
        messages.success(request, "Message sent successfully!")
        return redirect("planner:contact")
    return render(request, "planner/contact.html")


def coaching(request):
    return render(request, "planner/coaching.html")


def pricing(request):
    return render(request, "planner/pricing.html")


def services(request):
    return render(request, "planner/services.html")


@login_required
def choose_plan(request, plan):
    valid_plans = ["free", "pro", "elite"]
    if plan not in valid_plans:
        messages.error(request, "Invalid plan selected.")
        return redirect("planner:pricing")
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.plan = plan
    if plan == "free":
        profile.subscription_active = True
        profile.save()
        messages.success(request, "Free plan activated successfully!")
        return redirect("planner:dashboard")
    profile.subscription_active = False
    profile.save()
    return redirect("planner:payment_page", plan=plan)


@login_required
def payment_page(request, plan):
    valid_plans = ["free", "pro", "elite"]
    if plan not in valid_plans:
        messages.error(request, "Invalid payment plan.")
        return redirect("planner:pricing")
    return render(request, "pricing/payment_page.html", {"plan": plan})


@login_required
def payment_success(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.subscription_active = True
    profile.save()
    messages.success(request, f"{profile.plan.title()} plan activated successfully!")
    return render(request, "pricing/payment_success.html")


def free_plan(request):
    return render(request, "pricing/free_plan.html")


def pro_plan(request):
    return render(request, "pricing/pro_plan.html")


def elite_plan(request):
    return render(request, "pricing/elite_plan.html")


@login_required
def dashboard(request):
    return render(request, "planner/dashboard.html")


@login_required
def analytics(request):
    total_players = Player.objects.count()
    total_sessions = TrainingSession.objects.count()
    completed_sessions = TrainingSession.objects.filter(completed=True).count()
    attendance_records = Attendance.objects.count()
    performances = PlayerPerformance.objects.all()
    return render(request, "planner/analytics.html", {
        "total_players": total_players,
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "attendance_records": attendance_records,
        "performances": performances,
    })


@login_required
def team_dashboard(request):
    return render(request, "planner/team_dashboard.html")


@login_required
def my_sessions(request):
    sessions = TrainingSession.objects.all().order_by("-date")
    return render(request, "planner/my_sessions.html", {
        "sessions": sessions,
        "total_sessions": sessions.count(),
        "completed_sessions": sessions.filter(completed=True).count(),
    })


@login_required
def my_progress(request):
    return render(request, "planner/my_progress.html")


@login_required
def session_detail(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    return render(request, "planner/session_detail.html", {"session": session})


@login_required
@coach_required
def session_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        date = request.POST.get("date")
        duration = request.POST.get("duration")
        notes = request.POST.get("notes")
        if title and date:
            session = TrainingSession.objects.create(title=title, date=date, duration=duration, notes=notes)
            messages.success(request, "Training session created successfully!")
            return redirect("planner:session_detail", pk=session.pk)
        messages.error(request, "Title and date are required.")
    return render(request, "planner/session_form.html")


@login_required
@coach_required
def session_complete(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    session.completed = True
    session.save()
    messages.success(request, "Session marked as completed.")
    return redirect("planner:session_detail", pk=pk)


@login_required
@coach_required
def add_player(request):
    if request.method == "POST":
        team_name = request.POST.get("team_name", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        position = request.POST.get("position", "").strip()

        if team_name and first_name and last_name and position:
            team, _ = Team.objects.get_or_create(name=team_name)
            Player.objects.create(team=team, first_name=first_name, last_name=last_name, position=position)
            messages.success(request, f"Player {first_name} {last_name} added successfully!")
        else:
            messages.error(request, "All fields are required.")

        return redirect("planner:add_player")

    players = Player.objects.select_related("team").order_by("last_name")
    return render(request, "services/add_player.html", {"players": players})


@login_required
@coach_required
def delete_player(request, id):
    player = get_object_or_404(Player, id=id)
    if request.method == "POST":
        player.delete()
        messages.success(request, "Player deleted successfully!")
        return redirect("planner:add_player")
    return render(request, "services/delete_player.html", {"player": player})


@login_required
@coach_required
def mark_attendance(request):
    sessions = TrainingSession.objects.all().order_by("-date")
    players = Player.objects.all().order_by("last_name")
    if request.method == "POST":
        session_id = request.POST.get("session")
        session = get_object_or_404(TrainingSession, id=session_id)
        for player in players:
            status = request.POST.get(f"status_{player.id}")
            if status:
                Attendance.objects.update_or_create(session=session, player=player, defaults={"status": status})
        messages.success(request, "Attendance saved successfully!")
        return redirect("planner:dashboard")
    return render(request, "services/mark_attendance.html", {"sessions": sessions, "players": players})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role", "player")
        allowed_roles = ["coach", "parent", "player"]
        if role not in allowed_roles:
            role = "player"
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("planner:register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("planner:register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("planner:register")
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user, role=role)
        login(request, user)
        messages.success(request, f"Welcome, {username}! Your account was created.")
        return redirect("planner:dashboard")
    return render(request, "planner/register.html")


def real_app_features(request):
    return render(request, "services/real_app_features.html")


def planner_team_management(request):
    return render(request, "services/team_management.html")


def services_team_management(request):
    return render(request, "services/team_management.html")


def season_planner(request):
    return render(request, "services/season_planner.html")


def training_planner(request):
    return render(request, "services/training_planner.html")


def sessions_2d3d(request):
    return render(request, "services/sessions_2d3d.html")


def drill_library(request):
    return render(request, "services/drill_library.html")


def player_tracking(request):
    return render(request, "services/player_tracking.html")


@login_required
@coach_required
def training_builder(request):
    return render(request, "services/training_builder.html")


@login_required
@coach_required
def sessions_builder(request):
    return render(request, "services/session_builder.html")


def player_detail(request, id):
    return render(request, "services/player_detail.html", {"player_id": id})


@login_required
@coach_required
def advanced_analytics(request):
    return render(request, "services/advanced_analytics.html")


@login_required
@coach_required
def coaching_system(request):
    teams = Team.objects.prefetch_related(
        "players",
        "seasons__weekly_goals__sessions__session_drills__drill",
        "seasons__weekly_goals__sessions__attendance",
        "seasons__weekly_goals__sessions__performances",
    )
    return render(request, "planner/coaching_system.html", {"teams": teams})