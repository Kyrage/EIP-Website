# Generated by Django 3.1.7 on 2021-04-02 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('registered', models.BooleanField(blank=True, default=False, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Newsletter',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='post')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Publication',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alpha', models.BooleanField(blank=True, default=False, null=True)),
                ('beta', models.BooleanField(blank=True, default=False, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edit', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Alpha / Beta',
            },
        ),
    ]
