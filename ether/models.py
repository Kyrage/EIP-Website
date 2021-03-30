from django.db import models
from django.conf import settings
from django.utils import timezone

class Newsletter(models.Model):
    author = models.EmailField(max_length=254)
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
        return (('User: {0}').format(self.author))

    class Meta:
        verbose_name_plural = 'Subscribe to the newsletter'
