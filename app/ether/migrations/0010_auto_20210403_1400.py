# Generated by Django 3.1.7 on 2021-04-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0009_auto_20210403_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
