from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # fields = ('email','friendly_name', 'address', 'phone')
    list_display = ('email', 'is_staff', 'is_active', 'friendly_name')
    list_filter = ('email', 'is_staff', 'is_active',)
    list_editable = ('friendly_name',) #  'address', 'phone',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'friendly_name', 'address', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'friendly_name', 'address', 'phone')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
