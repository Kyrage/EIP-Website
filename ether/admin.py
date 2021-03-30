from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Newsletter)

admin.site.unregister(Group)
