# Generated by Django 4.0.4 on 2022-07-15 10:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ether', '0036_shoptexture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfriends',
            name='name',
        ),
        migrations.AddField(
            model_name='userfriends',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
