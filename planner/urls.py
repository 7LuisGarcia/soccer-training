from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.contrib.auth import views as auth_views 

app_name = "planner"

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # MAIN PAGES
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("coaching/", views.coaching, name="coaching"),
    path("pricing/", views.pricing, name="pricing"),
    path("services/", views.services, name="services"),

    # AUTH
    path("login/", LoginView.as_view(template_name="planner/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="planner:home"), name="logout"),
    path("register/", views.register, name="register"),
    # PASSWORD RESET
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="planner/password_reset_form.html",
        email_template_name="planner/password_reset_email.html",
        subject_template_name="planner/password_reset_subject.txt",
        success_url="done/"
    ),
    name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="planner/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="planner/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),
    path("analytics/", views.analytics, name="analytics"),
    path("team-dashboard/", views.team_dashboard, name="team_dashboard"),
    path("my-sessions/", views.my_sessions, name="my_sessions"),
    path("my-progress/", views.my_progress, name="my_progress"),

    # SESSIONS
    path("session/new/", views.session_create, name="session_create"),
    path("session/<int:pk>/", views.session_detail, name="session_detail"),
    path("session/<int:pk>/complete/", views.session_complete, name="session_complete"),

    # PLANNER
    path("team-management/", views.planner_team_management, name="team_management"),
    path("season-planner/", views.season_planner, name="season_planner"),
    path("training-planner/", views.training_planner, name="training_planner"),
    path("sessions-2d3d/", views.sessions_2d3d, name="sessions_2d3d"),
    path("drill-library/", views.drill_library, name="drill_library"),

    # SERVICES
    path("player-tracking/", views.player_tracking, name="player_tracking"),
    path("training-builder/", views.training_builder, name="training_builder"),
    path("sessions-builder/", views.sessions_builder, name="sessions_builder"),
    path("session-builder/", views.sessions_builder, name="session_builder"),
    path("services/team-management/", views.services_team_management, name="services_team_management"),

    # PLAYERS
    path("player/<int:id>/", views.player_detail, name="player_detail"),
    path("players/add/", views.add_player, name="add_player"),
    path("players/<int:id>/delete/", views.delete_player, name="delete_player"),
    path("attendance/mark/", views.mark_attendance, name="mark_attendance"),

    # EXTRA FEATURES
    path("advanced-analytics/", views.advanced_analytics, name="advanced_analytics"),
    path("real-app-features/", views.real_app_features, name="real_app_features"),
    path("coaching-system/", views.coaching_system, name="coaching_system"),

    # PRICING / PAYMENTS
    path("pricing/free/", views.free_plan, name="free_plan"),
    path("pricing/pro/", views.pro_plan, name="pro_plan"),
    path("pricing/elite/", views.elite_plan, name="elite_plan"),
    path("choose-plan/<str:plan>/", views.choose_plan, name="choose_plan"),
    path("payment/<str:plan>/", views.payment_page, name="payment_page"),
    path("payment-success/", views.payment_success, name="payment_success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)