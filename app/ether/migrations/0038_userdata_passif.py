# Generated by Django 4.0.4 on 2022-09-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0037_remove_userfriends_name_userfriends_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='passif',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
