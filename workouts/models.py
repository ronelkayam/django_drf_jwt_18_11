from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Workout(models.Model):
    #קישור FK לטבלת המשתמשים המובנית של django
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='workouts')
    exercise_name = models.CharField(max_length=50)
    weight_kg = models.FloatField()
    reps = models.IntegerField()
    sets = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name}"


    def __repr__(self):
        pass


