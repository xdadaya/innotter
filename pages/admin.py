from django.contrib import admin
from django.contrib.auth.models import Group

from pages.models import Page, FollowRequest

admin.site.unregister(Group)
admin.site.register(Page)
admin.site.register(FollowRequest)
