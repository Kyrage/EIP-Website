# Generated by Django 3.1.7 on 2022-01-09 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0027_auto_20220109_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='mentoring',
            field=models.IntegerField(default=1000),
        ),
    ]