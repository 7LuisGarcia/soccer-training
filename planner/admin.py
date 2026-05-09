from django.contrib import admin
from .models import (
    Team, Player, Season, WeeklyGoal, Drill,
    TrainingSession, SessionDrill, Attendance, PlayerPerformance
)

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(WeeklyGoal)
admin.site.register(Drill)
admin.site.register(TrainingSession)
admin.site.register(SessionDrill)
admin.site.register(Attendance)
admin.site.register(PlayerPerformance)
from .models import UserProfile

admin.site.register(UserProfile)
# Register your models here.
