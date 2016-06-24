from django.contrib import admin
from .models import User
from django.contrib.auth.models import Permission


admin.site.register(Permission)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'first_name', 'last_name', 'email','no_expediente','is_active','is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_superuser',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
            ('User', {'fields': ('username', 'password')}),
            ('Personal Info', {'fields': (
                'first_name',
                'last_name',
                'email',
                'avatar',
                'no_expediente',
             )}),
            ('Permissions', {'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
             )}),
        )
