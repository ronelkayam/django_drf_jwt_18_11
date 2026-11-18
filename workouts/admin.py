from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exercise_name', 'weight_kg', 'reps', 'created_at')
    list_filter = ('user', 'exercise_name')
    search_fields = ('exercise_name', 'user__username')