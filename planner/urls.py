from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'planner'

urlpatterns = [
    path('', views.home, name='home'),
    path('session/new/', views.session_create, name='session_create'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('session/<int:pk>/complete/', views.session_complete, name='session_complete'),
    path('contact/', views.contact, name='contact'),
    path('coaching/', views.coaching, name='coaching'),
    path('pricing/', views.pricing, name='pricing'),
    path('services/', views.services, name='services'),
    path('team-management/', views.team_management, name='team_management'),
    path('season-planner/', views.season_planner, name='season_planner'),
    path('training-planner/', views.training_planner, name='training_planner'),
    path('sessions-2d3d/', views.sessions_2d3d, name='sessions_2d3d'),
    path('drill-library/', views.drill_library, name='drill_library'),
    path('about/', views.about, name='about'),
]

# Add media serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
