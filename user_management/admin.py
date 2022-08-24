from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
