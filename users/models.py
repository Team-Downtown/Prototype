from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.views import generic

class MarketUser(AbstractUser):

    phoneNumber = models.CharField(max_length=12, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)
    bio = models.TextField(default='', blank=True)
    unreadMessages = models.IntegerField(default=0)


    def __str__(self):
        return self.username
