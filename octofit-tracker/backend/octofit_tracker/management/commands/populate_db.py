from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Team, Activity, Workout, Leaderboard, UserProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            Leaderboard.objects.all().delete()
            Team.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            marvel_admin = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password')
            dc_admin = User.objects.create_user(username='batman', email='batman@dc.com', password='password')

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Team Marvel', description='Marvel superheroes', created_by=marvel_admin)
            dc = Team.objects.create(name='Team DC', description='DC superheroes', created_by=dc_admin)

            marvel.members.add(marvel_admin)
            dc.members.add(dc_admin)

            users = [
                User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password'),
                User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='password'),
                User.objects.create_user(username='superman', email='superman@dc.com', password='password'),
                User.objects.create_user(username='wonderwoman', email='wonderwoman@dc.com', password='password'),
            ]
            marvel.members.add(users[0], users[1])
            dc.members.add(users[2], users[3])

            for user in [marvel_admin, users[0], users[1]]:
                UserProfile.objects.create(user=user, age=35, experience_level='advanced')
            for user in [dc_admin, users[2], users[3]]:
                UserProfile.objects.create(user=user, age=33, experience_level='advanced')

            self.stdout.write(self.style.SUCCESS('Creating activities and workouts...'))
            import datetime
            for user in [marvel_admin, users[0], users[1], dc_admin, users[2], users[3]]:
                for i in range(3):
                    Activity.objects.create(
                        user=user,
                        activity_type='running',
                        title=f'Run {i+1}',
                        description='Superhero run',
                        duration_minutes=30+i*5,
                        calories_burned=300+i*10,
                        distance_km=5.0+i,
                        intensity='high',
                        activity_date=datetime.datetime.now(),
                        team=marvel if user in [marvel_admin, users[0], users[1]] else dc
                    )
                    Workout.objects.create(
                        user=user,
                        title=f'Workout {i+1}',
                        description='Superhero workout',
                        difficulty='advanced',
                        duration_minutes=45+i*5,
                        exercises=[{"name": "Pushups", "reps": 20+i*5}],
                        estimated_calories=400+i*20
                    )

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel, user=marvel_admin, total_calories_burned=900, total_distance_km=15, total_activities=9, rank=1)
            Leaderboard.objects.create(team=dc, user=dc_admin, total_calories_burned=850, total_distance_km=14, total_activities=9, rank=2)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
