from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username


class LandingPageImages(models.Model):
    ID = models.AutoField(primary_key=True)
    PictureLinkName = models.TextField(max_length=100)
    PictureLink = models.FilePathField()
    DescText = models.TextField(max_length=600, default=0)
