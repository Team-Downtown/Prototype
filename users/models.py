from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class MarketUser(AbstractUser):

    phoneNumber = models.CharField(max_length=12, default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    bio = models.TextField(default='')


    def __str__(self):
        return self.username
        #return self.first_name
