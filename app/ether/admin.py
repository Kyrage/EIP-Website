from django_simple_cookie_consent.models import CookieConsentSettings
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from taggit.admin import Tag
from django import forms
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

class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = 'UserData'
    fk_name = 'user'

class UserSkillsInline(admin.StackedInline):
    model = UserSkills
    can_delete = False
    verbose_name_plural = 'UserData'
    fk_name = 'user'

class UserInventoryInline(admin.StackedInline):
    model = UserInventory
    can_delete = False
    verbose_name_plural = 'Inventory'
    fk_name = 'user'

class UserFriendsInline(admin.StackedInline):
    model = UserFriends
    can_delete = False
    verbose_name_plural = 'Friends'
    fk_name = 'user'

class UserGuildInline(admin.StackedInline):
    model = UserGuild
    can_delete = False
    verbose_name_plural = 'Guild'
    fk_name = 'user'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline, UserDataInline, UserSkillsInline, UserInventoryInline, UserFriendsInline, UserGuildInline,)

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

class UserTextureForm(forms.ModelForm):

    texture = forms.FileField(required=False)

    def save(self, commit=True):
        if self.cleaned_data.get('texture') is not None:
            data = self.cleaned_data['texture'].file.read()
            self.instance.texture = data
        return self.instance

    def save_m2m(self):
        pass

    class Meta:
        model = UserTexture
        fields = ['user', 'id', 'texture']


class UserTextureAdmin(admin.ModelAdmin):
    form = UserTextureForm
    list_display = ('user', 'id', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        return obj.preview

    preview.short_description = 'Preview Texture'
    preview.allow_tags = True

class ShopTextureForm(forms.ModelForm):

    texture = forms.FileField(required=False)

    def save(self, commit=True):
        if self.cleaned_data.get('texture') is not None:
            data = self.cleaned_data['texture'].file.read()
            self.instance.texture = data
        return self.instance

    def save_m2m(self):
        pass

    class Meta:
        model = ShopTexture
        fields = ['seller', 'id', 'texture', 'price']

class ShopTextureAdmin(admin.ModelAdmin):
    form = ShopTextureForm
    list_display = ('seller', 'id', 'price', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        return obj.preview

    preview.short_description = 'Preview Texture'
    preview.allow_tags = True

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Tag)
admin.site.unregister(CookieConsentSettings)

admin.site.register(User, UserAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserData)
admin.site.register(UserSkills)
admin.site.register(UserInventory)
#admin.site.register(UserFriends)
#admin.site.register(UserGuild)
#admin.site.register(UserMatchmaking)
admin.site.register(UserTexture, UserTextureAdmin)
admin.site.register(ShopTexture, ShopTextureAdmin)