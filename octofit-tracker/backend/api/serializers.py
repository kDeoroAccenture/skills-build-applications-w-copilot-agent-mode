from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Activity, Workout, Leaderboard, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'age', 'weight_kg', 'height_cm', 'fitness_goal', 
                  'experience_level', 'avatar', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    created_by = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'members', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model - converts ObjectId to strings"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'title', 'description', 'duration_minutes', 
                  'calories_burned', 'distance_km', 'intensity', 'activity_date', 'team',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'title', 'description', 'difficulty', 'duration_minutes', 
                  'exercises', 'estimated_calories', 'is_completed', 'completed_at',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'team', 'user', 'total_calories_burned', 'total_distance_km', 
                  'total_activities', 'rank', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
