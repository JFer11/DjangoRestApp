from django.db import models
from django.contrib.auth.models import User


# Create your models here.
"""
class User(models.Model):
    name = models.CharField(max_length=30)
    birth = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    gender = models.BooleanField()

    JUNIOR = 'JR'
    MID_LEVEL = 'MID'
    SENIOR = 'SR'
    LEVEL = (
        (JUNIOR, 'Junior'),
        (MID_LEVEL, 'Mid-level'),
        (SENIOR, 'Senior')
    )
    level = models.CharField(max_length=3, choices=LEVEL)

    def __str__(self):
        return self.name
"""


class Article(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
