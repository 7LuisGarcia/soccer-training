from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("coach", "Coach"),
        ("parent", "Parent"),
        ("player", "Player"),
    ]

    PLAN_CHOICES = [
        ("free", "Free"),
        ("pro", "Pro"),
        ("elite", "Elite"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="player"
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="free"
    )

    subscription_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.plan}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="players"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Season(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="seasons"
    )

    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class WeeklyGoal(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="weekly_goals"
    )

    week_number = models.PositiveIntegerField()
    goal = models.CharField(max_length=200)

    def __str__(self):
        return f"Week {self.week_number}: {self.goal}"


class TrainingSession(models.Model):
    weekly_goal = models.ForeignKey(
        WeeklyGoal,
        on_delete=models.CASCADE,
        related_name="sessions",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    date = models.DateField()

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes",
        default=60
    )

    focus = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    notes = models.TextField(blank=True, null=True)

    completed = models.BooleanField(default=False)

    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.date})"


class Drill(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=100)

    category = models.CharField(
        max_length=100,
        default="General"
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="medium"
    )

    duration_minutes = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title


class SessionDrill(models.Model):
    session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name="session_drills"
    )

    drill = models.ForeignKey(
        Drill,
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(default=1)

    duration_minutes = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.session} - {self.drill}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("injured", "Injured"),
        ("excused", "Excused"),
    ]

    session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="present"
    )

    def __str__(self):
        return f"{self.player} - {self.status}"


class PlayerPerformance(models.Model):
    session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField(default=5)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.player} - {self.rating}/10"