from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    profile_picture = models.ImageField(upload_to='user_profile_pics/',
                                        default='user_profile_pics/default-profile-picture.jpg')
