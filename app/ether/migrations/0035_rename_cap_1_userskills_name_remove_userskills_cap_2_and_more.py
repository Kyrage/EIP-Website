# Generated by Django 4.0.4 on 2022-05-10 16:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0034_alter_userinventory_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userskills',
            old_name='cap_1',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='userskills',
            name='cap_2',
        ),
        migrations.RemoveField(
            model_name='userskills',
            name='cap_3',
        ),
        migrations.RemoveField(
            model_name='userskills',
            name='cap_4',
        ),
        migrations.AddField(
            model_name='userskills',
            name='_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userskills',
            name='_parentId',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userskills',
            name='equipped',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AddField(
            model_name='userskills',
            name='level',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.DeleteModel(
            name='UserPositions',
        ),
    ]
