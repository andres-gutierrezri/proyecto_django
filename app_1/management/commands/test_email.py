"""
Comando de management para probar el sistema de email.
Uso: python manage.py test_email [email_destino]
"""
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from app_1.utils import (
    send_verification_email,
    send_password_reset_email,
    send_password_changed_email,
    send_account_deleted_email
)

User = get_user_model()


class MockRequest:
    """Mock request object para simular peticiones HTTP en pruebas"""
    def __init__(self):
        self.META = {
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Test Browser)',
            'REMOTE_ADDR': '127.0.0.1',
            'HTTP_HOST': 'localhost:8000'
        }
    
    def build_absolute_uri(self, path):
        return f"http://localhost:8000{path}"


class Command(BaseCommand):
    help = 'Prueba el sistema de correo electrónico'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            nargs='?',
            type=str,
            help='Email de destino (opcional, usa el primer usuario si no se especifica)'
        )
        parser.add_argument(
            '--type',
            type=str,
            default='simple',
            choices=['simple', 'verification', 'password_reset', 'password_changed', 'account_deleted', 'all'],
            help='Tipo de email a enviar'
        )

    def handle(self, *args, **options):
        # Configuración actual
        self.stdout.write(self.style.SUCCESS('\n=== CONFIGURACIÓN DE EMAIL ==='))
        self.stdout.write(f"IS_DEPLOYED: {settings.IS_DEPLOYED}")
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        
        if settings.IS_DEPLOYED:
            self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
            self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        else:
            self.stdout.write(self.style.WARNING(
                "⚠️  Modo desarrollo - Los emails se mostrarán en la consola"
            ))

        # Determinar email destino
        email = options['email']
        if not email:
            # Usar el primer usuario disponible
            try:
                user = User.objects.first()
                if not user:
                    raise CommandError('No hay usuarios en la base de datos. Crea uno primero.')
                email = user.email
                self.stdout.write(f"\n✓ Usando email del primer usuario: {email}")
            except Exception as e:
                raise CommandError(f'Error al obtener usuario: {str(e)}')
        else:
            # Buscar el usuario por email
            try:
                user = User.objects.get(email=email)
                self.stdout.write(f"\n✓ Usuario encontrado: {user.get_full_name()}")
            except User.DoesNotExist:
                # Crear un objeto mock para pruebas simples
                self.stdout.write(self.style.WARNING(
                    f"⚠️  Usuario con email {email} no existe. Se usará para prueba simple solamente."
                ))
                user = None

        email_type = options['type']

        # Función auxiliar para enviar y reportar
        def send_and_report(email_name, send_func):
            self.stdout.write(f"\n📧 Enviando email: {email_name}")
            try:
                send_func()
                self.stdout.write(self.style.SUCCESS(f"✓ {email_name} enviado exitosamente"))
                return True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error al enviar {email_name}: {str(e)}"))
                return False

        # Enviar según el tipo
        success_count = 0
        total_count = 0

        if email_type == 'simple' or email_type == 'all':
            total_count += 1
            if send_and_report('Email Simple', lambda: send_mail(
                'Prueba de Email - Django',
                'Este es un mensaje de prueba del sistema de correo.\n\nSi recibes este mensaje, el sistema de email está funcionando correctamente.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )):
                success_count += 1

        if user and (email_type == 'verification' or email_type == 'all'):
            total_count += 1
            if send_and_report('Email de Verificación', lambda: send_verification_email(user, MockRequest())):
                success_count += 1

        if user and (email_type == 'password_reset' or email_type == 'all'):
            total_count += 1
            if send_and_report('Email de Restablecimiento de Contraseña', lambda: send_password_reset_email(user, 'token-ejemplo-123456')):
                success_count += 1

        if user and (email_type == 'password_changed' or email_type == 'all'):
            total_count += 1
            if send_and_report('Email de Contraseña Cambiada', lambda: send_password_changed_email(user, MockRequest())):
                success_count += 1

        if user and (email_type == 'account_deleted' or email_type == 'all'):
            total_count += 1
            if send_and_report('Email de Cuenta Eliminada', lambda: send_account_deleted_email(user, MockRequest())):
                success_count += 1

        # Resumen
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(self.style.SUCCESS(f"✓ Emails enviados exitosamente: {success_count}/{total_count}"))
        if success_count < total_count:
            self.stdout.write(self.style.ERROR(f"✗ Emails fallidos: {total_count - success_count}/{total_count}"))
        
        if not settings.IS_DEPLOYED:
            self.stdout.write(self.style.WARNING(
                "\n💡 Recuerda: Estás en modo desarrollo. "
                "Los emails aparecen en la consola del servidor, no se envían realmente."
            ))
        
        self.stdout.write(f"{'='*50}\n")
