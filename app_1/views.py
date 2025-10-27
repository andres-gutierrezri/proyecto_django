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

from .forms import CustomUserRegistrationForm, CustomAuthenticationForm
from .models import CustomUser
from .utils import (
    send_verification_email,
    send_login_notification_email
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
                    messages.error(
                        request,
                        'No existe una cuenta con este correo electrónico. '
                        '¿Deseas registrarte?'
                    )
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'app_1/page_login.html', context)


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('page_login')


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
    """
    context = {
        'user': request.user,
    }

    return render(request, 'app_1/dashboard.html', context)

