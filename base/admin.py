from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'auth_provider', 'is_staff', 'is_active', 'bio', 'date_joined', 'avi', 'isPrivate')
    list_filter = ('email', 'username', 'is_staff', 'is_active', 'auth_provider',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('bio', 'date_joined', 'avi', 'auth_provider')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'isPrivate')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'isPrivate','user_permissions', 'bio', 'avi', 'auth_provider'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined',)  # Make date_joined non-editable



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Income)
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Savings)