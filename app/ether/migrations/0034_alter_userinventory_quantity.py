# Generated by Django 4.0.4 on 2022-05-10 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ether', '0033_rename_item_userinventory_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinventory',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
