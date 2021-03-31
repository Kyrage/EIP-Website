from django.contrib import admin
from django.contrib.auth.models import Group
from taggit.admin import Tag
from .models import *

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'registered')

class GameAdmin(admin.ModelAdmin):
    list_display = ('author', 'alpha', 'beta')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_date', 'last_edit')

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)

admin.site.unregister(Group)
admin.site.unregister(Tag)
