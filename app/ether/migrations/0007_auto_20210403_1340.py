# Generated by Django 3.1.7 on 2021-04-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0006_auto_20210403_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
