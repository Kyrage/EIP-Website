# Generated by Django 4.0.4 on 2022-09-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0038_userdata_passif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='mentoring',
            field=models.IntegerField(default=0),
        ),
    ]