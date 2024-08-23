from django.db import models

class Usages(models.Model):
    ts = models.DateTimeField()
    thing = models.CharField(max_length=200)
    data = models.FloatField()