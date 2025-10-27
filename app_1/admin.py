"""
Configuración del panel de administración de Django.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Configuración del panel de administración para CustomUser."""

    model = CustomUser
    list_display = [
        'email',
        'first_name',
        'last_name',
        'email_verified',
        'is_staff',
        'is_active',
        'date_joined'
    ]
    list_filter = [
        'is_staff',
        'is_active',
        'email_verified',
        'date_joined'
    ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'username')
        }),
        ('Verificación', {
            'fields': (
                'email_verified',
                'email_verification_token',
                'email_verification_sent_at'
            )
        }),
        ('Restablecimiento de Contraseña', {
            'fields': (
                'password_reset_token',
                'password_reset_sent_at'
            ),
            'classes': ('collapse',)  # Colapsar por defecto
        }),
        ('Preferencias', {
            'fields': ('notify_on_login', 'newsletter_subscription')
        }),
        ('Términos', {
            'fields': ('terms_accepted',)
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
