from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to='profile', default='/profile/noAvatar.jpg')
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = 'Profile'

class Newsletter(models.Model):
    email = models.EmailField(max_length=254)
    registered = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = 'Newsletter'

class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    alpha = models.BooleanField(blank=True, null=True, default=False)
    beta = models.BooleanField(blank=True, null=True, default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Alpha / Beta'

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    img = models.ImageField(upload_to='post')
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Publication'

# Get From API

class UserSkills(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    cap_1 = models.CharField(max_length=250)
    cap_2 = models.CharField(max_length=250)
    cap_3 = models.CharField(max_length=250)
    cap_4 = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Skills'

class UserPositions(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    map = models.CharField(max_length=250)
    x = models.CharField(max_length=250)
    y = models.CharField(max_length=250)
    z = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Position'

class UserInventory(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    item = models.CharField(max_length=250)
    number = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Inventory'

class UserFriends(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Friends'

class UserGuild(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.author)

    class Meta:
        verbose_name_plural = 'Guild'
