from django.contrib import admin
from .models import Team, Activity, Workout, Leaderboard, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'experience_level', 'fitness_goal', 'created_at']
    list_filter = ['experience_level', 'created_at']
    search_fields = ['user__username', 'fitness_goal']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'title', 'duration_minutes', 'calories_burned', 'activity_date']
    list_filter = ['activity_type', 'intensity', 'activity_date', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'activity_type', 'title', 'description')
        }),
        ('Metrics', {
            'fields': ('duration_minutes', 'calories_burned', 'distance_km', 'intensity')
        }),
        ('Additional', {
            'fields': ('activity_date', 'team', 'created_at', 'updated_at')
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'difficulty', 'duration_minutes', 'is_completed', 'created_at']
    list_filter = ['difficulty', 'is_completed', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Workout Information', {
            'fields': ('user', 'title', 'description', 'difficulty')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'exercises', 'estimated_calories')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['team', 'user', 'total_calories_burned', 'total_distance_km', 'rank']
    list_filter = ['team', 'rank', 'created_at']
    search_fields = ['team__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
