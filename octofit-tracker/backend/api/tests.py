from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Team, Activity, Workout, UserProfile


class UserAPITestCase(APITestCase):
    """Test cases for User API"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()

    def test_user_list(self):
        """Test user list endpoint"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        """Test user detail endpoint"""
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class TeamAPITestCase(APITestCase):
    """Test cases for Team API"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        """Test creating a team"""
        data = {
            'name': 'Test Team',
            'description': 'Test Description'
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Team')

    def test_team_list(self):
        """Test team list endpoint"""
        Team.objects.create(name='Team 1', created_by=self.user)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        """Test creating an activity"""
        from django.utils import timezone
        data = {
            'activity_type': 'running',
            'title': 'Morning Run',
            'duration_minutes': 30,
            'calories_burned': 300,
            'distance_km': 5.0,
            'intensity': 'high',
            'activity_date': timezone.now()
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Morning Run')

    def test_my_activities(self):
        """Test getting user's activities"""
        response = self.client.get('/api/activities/my_activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITestCase(APITestCase):
    """Test cases for Workout API"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_workout(self):
        """Test creating a workout"""
        data = {
            'title': 'Full Body Workout',
            'description': 'Complete full body exercise routine',
            'difficulty': 'intermediate',
            'duration_minutes': 60,
            'exercises': ['push-ups', 'squats', 'deadlifts'],
            'estimated_calories': 500
        }
        response = self.client.post('/api/workouts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Full Body Workout')

    def test_complete_workout(self):
        """Test completing a workout"""
        workout = Workout.objects.create(
            user=self.user,
            title='Test Workout',
            description='Test',
            difficulty='beginner',
            duration_minutes=30
        )
        response = self.client.post(f'/api/workouts/{workout.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_completed'])


class UserProfileAPITestCase(APITestCase):
    """Test cases for UserProfile API"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            age=25,
            weight_kg=70,
            experience_level='beginner'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_detail(self):
        """Test getting user profile"""
        response = self.client.get(f'/api/profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 25)
