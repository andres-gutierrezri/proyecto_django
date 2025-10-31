"""
Utilidades para la aplicación, incluyendo envío de emails.
"""
import secrets
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


def generate_verification_token():
    """Genera un token seguro para verificación de email."""
    return secrets.token_urlsafe(32)


def send_verification_email(user, request):
    """
    Envía un email de verificación al usuario.

    Args:
        user: Instancia del modelo CustomUser
        request: Objeto HttpRequest para construir URLs absolutas
    """
    # Generar token de verificación
    token = generate_verification_token()
    user.email_verification_token = token
    user.email_verification_sent_at = timezone.now()
    user.save(update_fields=[
        'email_verification_token',
        'email_verification_sent_at'
    ])

    # Construir URL de verificación
    verification_url = request.build_absolute_uri(
        f'/verify-email/{token}/'
    )

    # Crear mensaje de texto plano limpio y legible
    plain_message = f"""
Hola {user.get_full_name() or user.username},

Gracias por registrarte en Aplicación Web.

Para completar tu registro, por favor verifica tu correo electrónico haciendo clic en el siguiente enlace:

{verification_url}

Si no creaste una cuenta en Aplicación Web, puedes ignorar este correo.

Saludos,
El equipo de Aplicación Web
    """.strip()

    # Renderizar HTML solo en producción
    html_message = None
    if settings.IS_DEPLOYED:
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'Aplicación Web',
        }
        html_message = render_to_string(
            'app_1/emails/verification_email.html',
            context
        )

    # Enviar el email
    send_mail(
        subject='Verifica tu correo electrónico - Aplicación Web',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_login_notification_email(user, request):
    """
    Envía un email de notificación de inicio de sesión al usuario.

    Args:
        user: Instancia del modelo CustomUser
        request: Objeto HttpRequest para obtener información de la sesión
    """
    # Verificar si el usuario desea recibir notificaciones
    if not user.notify_on_login:
        return

    # Obtener información del request
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')
    login_time = timezone.now()

    # Crear mensaje de texto plano limpio y legible
    plain_message = f"""
Hola {user.get_full_name() or user.username},

Se ha detectado un nuevo inicio de sesión en tu cuenta.

Detalles del inicio de sesión:
- Fecha y hora: {login_time.strftime('%d/%m/%Y %H:%M')}
- Dirección IP: {ip_address}
- Dispositivo: {user_agent}

Si no reconoces esta actividad, te recomendamos cambiar tu contraseña inmediatamente.

Saludos,
El equipo de Aplicación Web
    """.strip()

    # Renderizar HTML solo en producción
    html_message = None
    if settings.IS_DEPLOYED:
        context = {
            'user': user,
            'login_time': login_time,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'site_name': 'Aplicación Web',
        }
        html_message = render_to_string(
            'app_1/emails/login_notification.html',
            context
        )

    # Enviar el email
    send_mail(
        subject='Nuevo inicio de sesión detectado - Aplicación Web',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,  # No fallar si el email no se puede enviar
    )

    # Actualizar la fecha de última notificación
    user.last_login_notification = timezone.now()
    user.save(update_fields=['last_login_notification'])


def get_client_ip(request):
    """
    Obtiene la dirección IP del cliente desde el request.

    Args:
        request: Objeto HttpRequest

    Returns:
        str: Dirección IP del cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_password_reset_email(user, request):
    """
    Envía un email con el enlace para restablecer la contraseña.

    Args:
        user: Instancia del modelo CustomUser
        request: Objeto HttpRequest para construir URLs absolutas
    """
    # Generar token de restablecimiento
    token = generate_verification_token()
    user.password_reset_token = token
    user.password_reset_sent_at = timezone.now()
    user.save(update_fields=[
        'password_reset_token',
        'password_reset_sent_at'
    ])

    # Construir URL de restablecimiento
    reset_url = request.build_absolute_uri(
        f'/password-reset-confirm/{token}/'
    )

    # Crear mensaje de texto plano limpio y legible
    plain_message = f"""
Hola {user.get_full_name() or user.username},

Recibimos una solicitud para restablecer la contraseña de tu cuenta en Aplicación Web.

Para restablecer tu contraseña, haz clic en el siguiente enlace:

{reset_url}

Este enlace es válido por 24 horas.

Si no solicitaste restablecer tu contraseña, puedes ignorar este correo. Tu contraseña actual seguirá siendo válida.

Saludos,
El equipo de Aplicación Web
    """.strip()

    # Renderizar HTML solo en producción
    html_message = None
    if settings.IS_DEPLOYED:
        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'Aplicación Web',
            'valid_hours': 24,  # El enlace será válido por 24 horas
        }
        html_message = render_to_string(
            'app_1/emails/password_reset_email.html',
            context
        )

    # Enviar el email
    send_mail(
        subject='Restablece tu contraseña - Aplicación Web',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_changed_email(user, request):
    """
    Envía un email de confirmación cuando la contraseña ha sido cambiada.

    Args:
        user: Instancia del modelo CustomUser
        request: Objeto HttpRequest para construir URLs absolutas
    """
    # Construir URL completa del sitio
    site_url = request.build_absolute_uri('/').rstrip('/')
    change_time = timezone.now()

    # Crear mensaje de texto plano limpio y legible
    plain_message = f"""
Hola {user.get_full_name() or user.username},

Tu contraseña ha sido actualizada exitosamente.

Detalles del cambio:
- Fecha y hora: {change_time.strftime('%d/%m/%Y %H:%M')}

Si no realizaste este cambio, contacta inmediatamente con nosotros en {site_url}

Saludos,
El equipo de Aplicación Web
    """.strip()

    # Renderizar HTML solo en producción
    html_message = None
    if settings.IS_DEPLOYED:
        context = {
            'user': user,
            'change_time': change_time,
            'site_name': 'Aplicación Web',
            'site_url': site_url,
        }
        html_message = render_to_string(
            'app_1/emails/password_changed_email.html',
            context
        )

    # Enviar el email
    send_mail(
        subject='Tu contraseña ha sido actualizada - Aplicación Web',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,  # No fallar si el email no se puede enviar
    )
