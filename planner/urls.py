from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import RegisterView

app_name = "planner"

urlpatterns = [
    path("", views.home, name="home"),

    # Sessions
    path("session/new/", views.session_create, name="session_create"),
    path("session/<int:pk>/", views.session_detail, name="session_detail"),
    path("session/<int:pk>/complete/", views.session_complete, name="session_complete"),

    # Main pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("coaching/", views.coaching, name="coaching"),
    path("pricing/", views.pricing, name="pricing"),
    path("services/", views.services, name="services"),

    # Planner pages
    path("team-management/", views.planner_team_management, name="team_management"),
    path("season-planner/", views.season_planner, name="season_planner"),
    path("training-planner/", views.training_planner, name="training_planner"),
    path("sessions-2d3d/", views.sessions_2d3d, name="sessions_2d3d"),
    path("drill-library/", views.drill_library, name="drill_library"),

    # Services
    path("player-tracking/", views.player_tracking, name="player_tracking"),
    path("training-builder/", views.training_builder, name="training_builder"),
    path("sessions-builder/", views.sessions_builder, name="sessions_builder"),
    path("services/team-management/", views.services_team_management, name="services_team_management"),

    # Players / dashboard
    path("player/<int:id>/", views.player_detail, name="player_detail"),
    path("team-dashboard/", views.team_dashboard, name="team_dashboard"),
    path("advanced-analytics/", views.advanced_analytics, name="advanced_analytics"),

    
    # Pricing plans
    path("pricing/free/", views.free_plan, name="free_plan"),
    path("pricing/pro/", views.pro_plan, name="pro_plan"),
    path("pricing/elite/", views.elite_plan, name="elite_plan"),

    # Auth
    path(
        "login/",
        LoginView.as_view(
            template_name="planner/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="planner/logged_out.html"),
        name="logout",
    ),
    path("register/", RegisterView.as_view(), name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)