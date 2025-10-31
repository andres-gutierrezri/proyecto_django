"""
Utilidades para la aplicación, incluyendo envío de emails.
"""
import secrets
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

    # Contexto para el template
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'Aplicación Web',
    }

    # Renderizar el email HTML
    html_message = render_to_string(
        'app_1/emails/verification_email.html',
        context
    )
    plain_message = strip_tags(html_message)

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

    # Contexto para el template
    context = {
        'user': user,
        'login_time': timezone.now(),
        'ip_address': ip_address,
        'user_agent': user_agent,
        'site_name': 'Aplicación Web',
    }

    # Renderizar el email HTML
    html_message = render_to_string(
        'app_1/emails/login_notification.html',
        context
    )
    plain_message = strip_tags(html_message)

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

    # Contexto para el template
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'Aplicación Web',
        'valid_hours': 24,  # El enlace será válido por 24 horas
    }

    # Renderizar el email HTML
    html_message = render_to_string(
        'app_1/emails/password_reset_email.html',
        context
    )
    plain_message = strip_tags(html_message)

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

    # Contexto para el template
    context = {
        'user': user,
        'change_time': timezone.now(),
        'site_name': 'Aplicación Web',
        'site_url': site_url,
    }

    # Renderizar el email HTML
    html_message = render_to_string(
        'app_1/emails/password_changed_email.html',
        context
    )
    plain_message = strip_tags(html_message)

    # Enviar el email
    send_mail(
        subject='Tu contraseña ha sido actualizada - Aplicación Web',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=True,  # No fallar si el email no se puede enviar
    )
