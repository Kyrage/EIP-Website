# Generated by Django 3.1.7 on 2021-09-06 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0023_auto_20210906_1233'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userdata',
            unique_together=set(),
        ),
    ]