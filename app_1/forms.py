"""
Formularios para autenticación y registro de usuarios.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    """
    Formulario de registro de usuario personalizado.
    Usa email como nombre de usuario y valida contraseñas complejas.
    """
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'tu correo electrónico',
            'id': 'emailverify'
        }),
        help_text='Tu correo electrónico también será tu nombre de usuario'
    )

    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'id': 'fname'
        })
    )

    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'id': 'lname'
        })
    )

    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'mínimo 8 caracteres',
            'id': 'userpassword'
        }),
        help_text=(
            'Tu contraseña debe tener entre 8 y 20 caracteres, contener '
            'letras mayúsculas y minúsculas, un carácter especial, y no debe '
            'contener espacios ni emojis.'
        )
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'confirma tu contraseña',
            'id': 'userpassword2'
        }),
        strip=False,
        help_text='Ingresa la misma contraseña para verificación.'
    )

    terms_accepted = forms.BooleanField(
        label='Acepto los términos y condiciones',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input',
            'id': 'terms'
        }),
        error_messages={
            'required': 'Debes aceptar antes de continuar'
        }
    )

    newsletter_subscription = forms.BooleanField(
        label='Suscribirme a boletines informativos',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input',
            'id': 'newsletter'
        })
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'terms_accepted',
            'newsletter_subscription'
        )

    def clean_email(self):
        """Valida que el email sea único y válido para Gmail."""
        email = self.cleaned_data.get('email')

        if email:
            email = email.lower().strip()

            # Verificar si el email ya existe
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError(
                    'Ya existe un usuario con este correo electrónico.'
                )

        return email

    def clean_password1(self):
        """Valida la contraseña usando todos los validadores configurados."""
        password = self.cleaned_data.get('password1')

        # Ejecutar todos los validadores de Django (incluido el personalizado)
        if password:
            validate_password(password, self.instance)

        return password

    def save(self, commit=True):
        """Guarda el usuario y configura campos adicionales."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower().strip()
        user.username = user.email  # Usar email como username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.terms_accepted = self.cleaned_data['terms_accepted']
        user.newsletter_subscription = self.cleaned_data.get(
            'newsletter_subscription',
            False
        )

        if commit:
            user.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de inicio de sesión personalizado.
    Usa email como nombre de usuario.
    """
    username = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'tu correo electrónico',
            'id': 'username',
            'autofocus': True
        })
    )

    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'contraseña',
            'id': 'password'
        })
    )

    remember_me = forms.BooleanField(
        label='Recordarme durante los próximos 30 días',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input',
            'id': 'rememberme'
        })
    )

    error_messages = {
        'invalid_login': (
            'Por favor ingresa un correo electrónico y contraseña correctos. '
            'Ten en cuenta que ambos campos pueden ser sensibles a mayúsculas '
            'y minúsculas.'
        ),
        'inactive': 'Esta cuenta está inactiva.',
    }

    def clean_username(self):
        """Normaliza el email a minúsculas."""
        username = self.cleaned_data.get('username')
        if username:
            return username.lower().strip()
        return username


class PasswordResetRequestForm(forms.Form):
    """
    Formulario para solicitar restablecimiento de contraseña.
    El usuario ingresa su email y recibe un enlace para restablecer.
    """
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'tu correo electrónico',
            'id': 'email',
            'autofocus': True
        }),
        help_text='Ingresa el correo electrónico asociado a tu cuenta'
    )

    def clean_email(self):
        """Normaliza el email a minúsculas."""
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email


class PasswordResetConfirmForm(forms.Form):
    """
    Formulario para establecer una nueva contraseña después de
    recibir el enlace de restablecimiento.
    """
    password1 = forms.CharField(
        label='Nueva contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'mínimo 8 caracteres',
            'id': 'password1',
            'autofocus': True
        }),
        help_text=(
            'Tu contraseña debe tener entre 8 y 20 caracteres, contener '
            'letras mayúsculas y minúsculas, un carácter especial, y no debe '
            'contener espacios ni emojis.'
        )
    )

    password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'confirma tu contraseña',
            'id': 'password2'
        }),
        strip=False,
        help_text='Ingresa la misma contraseña para verificación.'
    )

    def clean_password1(self):
        """Valida la contraseña usando todos los validadores configurados."""
        password = self.cleaned_data.get('password1')

        # Ejecutar todos los validadores de Django (incluido el personalizado)
        if password:
            validate_password(password)

        return password

    def clean(self):
        """Valida que las dos contraseñas coincidan."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                'Las dos contraseñas no coinciden.'
            )

        return cleaned_data