# Generated by Django 3.1.7 on 2021-09-04 08:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ether', '0016_auto_20210904_1038'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPosition',
            new_name='UserPositions',
        ),
    ]
