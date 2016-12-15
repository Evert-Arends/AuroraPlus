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


class Servers(models.Model):
    ID = models.AutoField(primary_key=True)
    User_ID = models.TextField(max_length=10)
    Server_key = models.TextField(max_length=255)
    Server_Name = models.TextField(max_length=50)
    Server_Description = models.TextField(max_length=255)
    Date_Added = models.DateField


class Messages(models.Model):
    ID = models.AutoField(primary_key=True)
    User_ID = models.TextField(max_length=10)
    Message_Name = models.TextField(max_length=20)
    Message_Text = models.TextField(max_length=500)
    Date_Received = models.DateField(auto_now=True)
    Message_Read = models.BooleanField(default=0)

