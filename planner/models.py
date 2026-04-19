from django.db import models

class TrainingSession(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.date})"


class Drill(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    session = models.ForeignKey(TrainingSession, related_name='drills', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    estimated_time = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()})"


class PerformanceNote(models.Model):
    session = models.ForeignKey(TrainingSession, related_name='performance_notes', on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.session} on {self.created_at.date()}"

