from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOEM

from .models import User


class UserAdmin(UserAdminOEM):
    fieldsets = None
    ordering = None
    list_display = ["legal_name", "email", "is_active"]
    list_filter = ["is_active"]


admin.site.register(User, UserAdmin)
