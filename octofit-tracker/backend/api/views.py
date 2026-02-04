from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Team, Activity, Workout, Leaderboard, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    ActivitySerializer, WorkoutSerializer, LeaderboardSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter by current user if authenticated"""
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.all()


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'member added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'member removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter activities by user or team"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        team_id = self.request.query_params.get('team_id', None)
        
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if team_id is not None:
            queryset = queryset.filter(team_id=team_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Filter workouts by user"""
        if self.request.user.is_authenticated:
            return Workout.objects.filter(user=self.request.user)
        return Workout.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, pk=None):
        """Mark workout as completed"""
        from django.utils import timezone
        workout = self.get_object()
        workout.is_completed = True
        workout.completed_at = timezone.now()
        workout.save()
        serializer = self.get_serializer(workout)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter leaderboard by team"""
        queryset = Leaderboard.objects.all()
        team_id = self.request.query_params.get('team_id', None)
        
        if team_id is not None:
            queryset = queryset.filter(team_id=team_id)
        
        return queryset

    @action(detail=False, methods=['get'])
    def team_leaderboard(self, request):
        """Get leaderboard for a specific team"""
        team_id = request.query_params.get('team_id', None)
        if team_id is None:
            return Response({'error': 'team_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        leaderboard = Leaderboard.objects.filter(team_id=team_id).order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
