from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager

class Newsletter(models.Model):
    email = models.EmailField(max_length=254)
    registered = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = 'Newsletter'

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()
    
    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Publication'
