from django.db import models

class Card(models.Model):
	dbf_id = models.IntegerField()
	name = models.CharField(max_length=100)
	player_class = models.CharField(max_length=20)