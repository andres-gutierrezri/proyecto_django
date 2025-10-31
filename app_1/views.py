"""
Vistas para autenticación y gestión de usuarios.
"""
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError

from .forms import (
    CustomUserRegistrationForm,
    CustomAuthenticationForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm
)
from .models import CustomUser, UserSession
from .utils import (
    send_verification_email,
    send_login_notification_email,
    send_password_reset_email,
    send_password_changed_email
)


@never_cache
@require_http_methods(["GET", "POST"])
def page_register(request):
    """
    Vista de registro de nuevos usuarios.
    Valida el formulario, crea el usuario y envía email de verificación.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            try:
                # Guardar el usuario
                user = form.save()

                # Enviar email de verificación
                try:
                    send_verification_email(user, request)
                    messages.success(
                        request,
                        f'¡Registro exitoso! Se ha enviado un correo de '
                        f'verificación a {user.email}. Por favor revisa tu '
                        f'bandeja de entrada.'
                    )
                except Exception as e:
                    # Si falla el envío del email, informar pero continuar
                    messages.warning(
                        request,
                        'Tu cuenta fue creada, pero hubo un problema al '
                        'enviar el correo de verificación. Por favor '
                        'contacta al soporte.'
                    )

                return redirect('page_login')

            except Exception as e:
                messages.error(
                    request,
                    'Ocurrió un error al crear tu cuenta. Por favor '
                    'intenta de nuevo.'
                )
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'app_1/page_register.html', context)


@never_cache
@require_http_methods(["GET", "POST"])
def page_login(request):
    """
    Vista de inicio de sesión.
    Autentica al usuario y envía notificación de login.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)

            # Autenticar usuario
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Iniciar sesión
                login(request, user)

                # Configurar duración de la sesión
                if remember_me:
                    # Recordar por 30 días
                    request.session.set_expiry(30 * 24 * 60 * 60)
                else:
                    # Sesión expira al cerrar el navegador
                    request.session.set_expiry(0)

                # Registrar sesión del usuario
                try:
                    from .utils import get_client_ip
                    UserSession.objects.create(
                        user=user,
                        session_key=request.session.session_key,
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                except Exception:
                    pass  # No interrumpir el login si falla el registro de sesión

                # Enviar notificación de login
                try:
                    send_login_notification_email(user, request)
                except Exception:
                    pass  # No interrumpir el login si falla el email

                messages.success(
                    request,
                    f'¡Bienvenido, {user.get_full_name()}!'
                )

                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(
                    request,
                    'Correo electrónico o contraseña incorrectos.'
                )
        else:
            # Usuario no registrado o cuenta inactiva
            email = request.POST.get('username', '').lower().strip()
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    if not user.is_active:
                        messages.error(
                            request,
                            'Tu cuenta está inactiva. Por favor contacta '
                            'al soporte.'
                        )
                    else:
                        messages.error(
                            request,
                            'Contraseña incorrecta.'
                        )
                except CustomUser.DoesNotExist:
                    from django.utils.safestring import mark_safe
                    messages.error(
                        request,
                        mark_safe(
                            'No existe una cuenta con este correo electrónico. '
                            '<a href="/register/" class="alert-link">¿Deseas registrarte?</a>'
                        )
                    )
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'app_1/page_login.html', context)


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """Vista para cerrar sesión y eliminar registro de sesión."""
    # Eliminar la sesión del registro antes de hacer logout
    if request.user.is_authenticated:
        try:
            session_key = request.session.session_key
            UserSession.objects.filter(
                user=request.user,
                session_key=session_key
            ).delete()
        except Exception:
            pass  # No interrumpir el logout si falla

    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('page_login')


@login_required
@require_http_methods(["POST"])
def terminate_session(request, session_key):
    """
    Vista para cerrar una sesión específica.
    Solo el propietario de la sesión puede cerrarla.
    """
    try:
        # Verificar que la sesión pertenece al usuario actual
        user_session = get_object_or_404(
            UserSession,
            user=request.user,
            session_key=session_key
        )

        # Verificar que no sea la sesión actual
        if session_key == request.session.session_key:
            messages.error(
                request,
                'No puedes cerrar tu sesión actual desde aquí. '
                'Usa el botón de cerrar sesión.'
            )
            return redirect('dashboard')

        # Eliminar la sesión de Django
        from django.contrib.sessions.models import Session
        try:
            Session.objects.get(session_key=session_key).delete()
        except Session.DoesNotExist:
            pass

        # Eliminar el registro de la sesión
        user_session.delete()

        messages.success(
            request,
            f'La sesión desde {user_session.get_device_info()} ha sido cerrada.'
        )

    except Exception as e:
        messages.error(
            request,
            'Hubo un problema al cerrar la sesión. '
            'Es posible que ya haya expirado.'
        )

    return redirect('dashboard')


@require_http_methods(["GET"])
def verify_email(request, token):
    """
    Vista para verificar el email del usuario usando el token.
    """
    user = get_object_or_404(
        CustomUser,
        email_verification_token=token
    )

    if user.email_verified:
        messages.info(request, 'Tu correo electrónico ya está verificado.')
    else:
        user.verify_email()
        messages.success(
            request,
            '¡Correo electrónico verificado exitosamente! Ya puedes '
            'iniciar sesión.'
        )

    return redirect('page_login')


@login_required
@require_http_methods(["GET"])
def dashboard(request):
    """
    Vista protegida del dashboard.
    Solo accesible para usuarios autenticados.
    Muestra información de sesiones activas.
    """
    # Limpiar sesiones inválidas
    UserSession.cleanup_invalid_sessions(request.user)

    # Obtener sesiones activas
    active_sessions = UserSession.objects.filter(user=request.user)

    # Detectar sesión actual
    current_session_key = request.session.session_key

    # Determinar si hay múltiples sesiones
    multiple_sessions = active_sessions.count() > 1

    context = {
        'user': request.user,
        'active_sessions': active_sessions,
        'current_session_key': current_session_key,
        'multiple_sessions': multiple_sessions,
        'sessions_count': active_sessions.count(),
    }

    return render(request, 'app_1/dashboard.html', context)


@never_cache
@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    """
    Vista para solicitar restablecimiento de contraseña.
    El usuario ingresa su email y recibe un enlace para restablecer.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                user = CustomUser.objects.get(email=email)

                # Enviar email de restablecimiento
                try:
                    send_password_reset_email(user, request)
                    messages.success(
                        request,
                        f'Se ha enviado un correo a {email} con instrucciones '
                        f'para restablecer tu contraseña. Por favor revisa tu '
                        f'bandeja de entrada.'
                    )
                except Exception as e:
                    messages.error(
                        request,
                        'Hubo un problema al enviar el correo. Por favor '
                        'intenta de nuevo más tarde.'
                    )

                # Redirigir siempre al login por seguridad
                # (no revelar si el email existe o no)
                return redirect('page_login')

            except CustomUser.DoesNotExist:
                # Por seguridad, mostrar el mismo mensaje incluso si el email no existe
                messages.success(
                    request,
                    f'Si existe una cuenta con el correo {email}, '
                    f'recibirás un email con instrucciones para restablecer '
                    f'tu contraseña.'
                )
                return redirect('page_login')

    else:
        form = PasswordResetRequestForm()

    context = {
        'form': form,
    }

    return render(request, 'app_1/password_reset_request.html', context)


@never_cache
@require_http_methods(["GET", "POST"])
def password_reset_confirm(request, token):
    """
    Vista para confirmar el restablecimiento de contraseña con el token.
    El usuario establece su nueva contraseña.
    """
    # Buscar el usuario con el token
    user = get_object_or_404(
        CustomUser,
        password_reset_token=token
    )

    # Verificar que el token no haya expirado (24 horas)
    from django.utils import timezone
    from datetime import timedelta

    if user.password_reset_sent_at:
        expiry_time = user.password_reset_sent_at + timedelta(hours=24)
        if timezone.now() > expiry_time:
            messages.error(
                request,
                'El enlace de restablecimiento ha expirado. Por favor '
                'solicita uno nuevo.'
            )
            return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password1')

            try:
                # Verificar que la nueva contraseña sea diferente a la anterior
                if user.check_password(password):
                    messages.error(
                        request,
                        'La nueva contraseña no puede ser igual a la anterior. '
                        'Por favor elige una contraseña diferente.'
                    )
                    # No limpiar el formulario, mantener el token válido
                    context = {
                        'form': form,
                        'token': token,
                        'user': user,
                    }
                    return render(request, 'app_1/password_reset_confirm.html', context)

                # Establecer la nueva contraseña
                user.set_password(password)

                # Limpiar el token de restablecimiento
                user.password_reset_token = None
                user.password_reset_sent_at = None
                user.save()

                # Enviar email de confirmación
                try:
                    send_password_changed_email(user, request)
                except Exception:
                    pass  # No interrumpir si falla el email

                messages.success(
                    request,
                    '¡Tu contraseña ha sido actualizada exitosamente! '
                    'Ya puedes iniciar sesión con tu nueva contraseña.'
                )

                return redirect('page_login')

            except Exception as e:
                messages.error(
                    request,
                    'Ocurrió un error al actualizar tu contraseña. '
                    'Por favor intenta de nuevo.'
                )
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = PasswordResetConfirmForm()

    context = {
        'form': form,
        'token': token,
        'user': user,
    }

    return render(request, 'app_1/password_reset_confirm.html', context)

