from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['id', 'name', 'email', 'is_staff', 'is_freelancer']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_freelancer')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 
                'email', 
                'password1', 
                'password2', 
                'is_staff', 
                'is_superuser', 
                'is_freelancer')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Address)
admin.site.register(models.Gig)
admin.site.register(models.Education)


