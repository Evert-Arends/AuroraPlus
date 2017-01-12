# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPageImages',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('PictureLinkName', models.TextField(max_length=100)),
                ('PictureLink', models.FilePathField()),
                ('DescText', models.TextField(default=0, max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('User_ID', models.TextField(max_length=10)),
                ('Message_Name', models.TextField(max_length=20)),
                ('Message_Text', models.TextField(max_length=500)),
                ('Date_Received', models.DateField(auto_now=True)),
                ('Message_Read', models.BooleanField(default=0)),
                ('Receive_Mail', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('User_ID', models.TextField(max_length=10)),
                ('Server_key', models.TextField(max_length=255)),
                ('Server_Name', models.TextField(max_length=50)),
                ('Server_Description', models.TextField(max_length=255)),
                ('Receive_Mail', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
