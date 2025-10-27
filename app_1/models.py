from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.
    Usa el email como nombre de usuario único para autenticación.
    """
    email = models.EmailField(
        'correo electrónico',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este correo electrónico.',
        }
    )

    # Campos adicionales para el usuario
    first_name = models.CharField('nombre', max_length=150, blank=False)
    last_name = models.CharField('apellido', max_length=150, blank=False)

    # Campo para verificación de email
    email_verified = models.BooleanField('email verificado', default=False)
    email_verification_token = models.CharField(
        'token de verificación',
        max_length=100,
        blank=True,
        null=True
    )
    email_verification_sent_at = models.DateTimeField(
        'fecha de envío de verificación',
        blank=True,
        null=True
    )

    # Campos para notificaciones de login
    notify_on_login = models.BooleanField(
        'notificar al iniciar sesión',
        default=True
    )
    last_login_notification = models.DateTimeField(
        'última notificación de login',
        blank=True,
        null=True
    )

    # Campos para restablecimiento de contraseña
    password_reset_token = models.CharField(
        'token de restablecimiento de contraseña',
        max_length=100,
        blank=True,
        null=True
    )
    password_reset_sent_at = models.DateTimeField(
        'fecha de envío de restablecimiento',
        blank=True,
        null=True
    )

    # Aceptación de términos y newsletter
    terms_accepted = models.BooleanField('términos aceptados', default=False)
    newsletter_subscription = models.BooleanField(
        'suscripción al boletín',
        default=False
    )

    # Usar email como nombre de usuario
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip()

    def send_verification_email(self):
        """Marca que se debe enviar email de verificación."""
        self.email_verification_sent_at = timezone.now()
        self.save(update_fields=['email_verification_sent_at'])

    def verify_email(self):
        """Marca el email como verificado."""
        self.email_verified = True
        self.email_verification_token = None
        self.save(update_fields=['email_verified', 'email_verification_token'])
