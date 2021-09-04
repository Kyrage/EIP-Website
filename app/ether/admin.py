from django_simple_cookie_consent.models import CookieConsentSettings
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from taggit.admin import Tag
from .models import *

class TokenInline(admin.StackedInline):
    model = Token
    can_delete = False
    verbose_name_plural = 'Token'
    fk_name = 'user'
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'registered')

class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'alpha', 'beta')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_date', 'last_edit')

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Tag)
#admin.site.unregister(CookieConsentSettings)

admin.site.register(User, UserAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserSkills)
