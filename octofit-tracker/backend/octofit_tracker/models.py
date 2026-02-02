from django.db import models
from django.contrib.auth import get_user_model

class Team(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.name

class Activity(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	type = models.CharField(max_length=100)
	duration = models.IntegerField()
	def __str__(self):
		return f"{self.user.username} - {self.type}"

class Leaderboard(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	points = models.IntegerField()
	def __str__(self):
		return f"{self.team.name}: {self.points}"

class Workout(models.Model):
	name = models.CharField(max_length=100)
	difficulty = models.CharField(max_length=50)
	def __str__(self):
		return self.name
