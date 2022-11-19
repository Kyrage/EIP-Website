from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.dispatch import receiver
from base64 import b64encode
from django.core.validators import MaxValueValidator, MinValueValidator

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

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=False, null=True)
    level = models.IntegerField(default=1)
    crystal = models.IntegerField(default=1000)
    cash = models.IntegerField(default=1000)
    mentoring = models.IntegerField(default=0)
    passif = models.CharField(max_length=25, blank=False, null=True)
    textureSlot = models.IntegerField(default=2)
    maxTextureSlot = models.IntegerField(default=10)
    hasDoneTutorial = models.BooleanField(default=False)
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
        verbose_name_plural = 'Data'

class UserSkills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _id = models.PositiveIntegerField(null=False, blank=False)
    _parentId = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    equipped = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(4)])
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
        verbose_name_plural = 'Skills'

class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _id = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    comment = models.CharField(max_length=250, null=True, blank=True)
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
        verbose_name_plural = 'Inventory'

class UserFriends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)

    def add_friend(self, friend):
        self.friends.add(friend)

    def remove_friend(self, friend):
        self.friends.remove(friend)

    @property
    def count_friends(self):
        return self.friends.count()

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Friends'

class UserGuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def edit(self):
        self.last_edit = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Guild'

class UserMatchmaking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Matchmaking'

class UserTexture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    texture = models.BinaryField(null=True, blank=True, editable=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Textures'

    @property
    def preview(self):
        if self.texture:
            return mark_safe('<img src="data:image;base64, {}" width="100" height="100" />'.format(b64encode(self.texture).decode('utf-8')))
        return ""

class ShopTexture(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    texture = models.BinaryField(null=True, blank=True, editable=True)
    price = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.seller)

    class Meta:
        verbose_name_plural = 'Commutary Textures Shop'

    @property
    def preview(self):
        if self.texture:
            return mark_safe('<img src="data:image;base64, {}" width="100" height="100" />'.format(b64encode(self.texture).decode('utf-8')))
        return ""

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Shop'

class UserDungeons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'User Dungeons'
