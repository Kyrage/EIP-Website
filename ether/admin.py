from django.contrib import admin
from django.contrib.auth.models import Group
from taggit.admin import Tag

from .models import *

admin.site.register(Newsletter)
admin.site.register(Post)

admin.site.unregister(Group)
admin.site.unregister(Tag)
