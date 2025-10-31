from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session


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


class UserSession(models.Model):
    """
    Modelo para rastrear sesiones activas de usuarios.
    Permite detectar múltiples sesiones simultáneas y gestionarlas.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='active_sessions',
        verbose_name='usuario'
    )
    session_key = models.CharField(
        'clave de sesión',
        max_length=40,
        unique=True
    )
    ip_address = models.GenericIPAddressField(
        'dirección IP',
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        'user agent',
        blank=True
    )
    created_at = models.DateTimeField(
        'fecha de creación',
        auto_now_add=True
    )
    last_activity = models.DateTimeField(
        'última actividad',
        auto_now=True
    )

    class Meta:
        verbose_name = 'sesión de usuario'
        verbose_name_plural = 'sesiones de usuario'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'session_key']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.session_key[:10]}..."

    def is_valid(self):
        """Verifica si la sesión de Django aún existe y es válida."""
        try:
            session = Session.objects.get(session_key=self.session_key)
            return session.expire_date > timezone.now()
        except Session.DoesNotExist:
            return False

    def get_device_info(self):
        """Extrae información básica del dispositivo desde el user agent."""
        ua = self.user_agent.lower()

        # Detectar sistema operativo
        if 'windows' in ua:
            os_name = 'Windows'
        elif 'mac' in ua or 'macintosh' in ua:
            os_name = 'macOS'
        elif 'linux' in ua:
            os_name = 'Linux'
        elif 'android' in ua:
            os_name = 'Android'
        elif 'iphone' in ua or 'ipad' in ua:
            os_name = 'iOS'
        else:
            os_name = 'Desconocido'

        # Detectar navegador
        if 'chrome' in ua and 'edg' not in ua:
            browser = 'Chrome'
        elif 'firefox' in ua:
            browser = 'Firefox'
        elif 'safari' in ua and 'chrome' not in ua:
            browser = 'Safari'
        elif 'edg' in ua:
            browser = 'Edge'
        elif 'opera' in ua or 'opr' in ua:
            browser = 'Opera'
        else:
            browser = 'Desconocido'

        return f"{browser} en {os_name}"

    @classmethod
    def cleanup_invalid_sessions(cls, user):
        """Elimina sesiones inválidas o expiradas para un usuario."""
        sessions = cls.objects.filter(user=user)
        for session in sessions:
            if not session.is_valid():
                session.delete()

