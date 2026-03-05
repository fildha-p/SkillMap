from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100)
    pass_percentage = models.IntegerField(default=70)
    total_levels = models.IntegerField(default=5)
    roles = models.ManyToManyField(Role, related_name='skills')

    def __str__(self):
        return self.name

class Question(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=
                                      [('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])
    difficulty_level = models.IntegerField() #`1 to 5

    def __str__(self):
        return f"{self.skill.name} - L{self.difficulty_level}"
    
class AssessmentAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    score = models.FloatField()
    level_achieved = models.IntegerField()
    passed = models.BooleanField(default=False)
    correct_count = models.IntegerField(default=0)      # NEW
    total_questions = models.IntegerField(default=0)    # NEW
    wrong_answers = models.JSONField(default=list, blank=True)  # NEW
    attempted_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField(default=0)  # in seconds

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} "
    
class UserSkillLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} - (L{self.level})"
    
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    readiness_score = models.FloatField(default=0)
    category = models.CharField(max_length=50, blank=True)
    selected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} → {self.role.name}"