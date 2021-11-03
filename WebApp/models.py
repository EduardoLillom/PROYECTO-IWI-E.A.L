from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    resolved_questions = models.IntegerField(default=0)
    punctuation = models.IntegerField(default=0)

class problema(models.Model):
    exercise = models.TextField()
    alternative = models.TextField()
    solution = models.CharField(max_length=1)
    times_tried = models.IntegerField()
    times_result = models.IntegerField()
    points = models.IntegerField()
    difficulty = models.IntegerField()