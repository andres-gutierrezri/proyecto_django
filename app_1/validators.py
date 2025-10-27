"""
Validadores personalizados para la aplicación.
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordComplexityValidator:
    """
    Valida que la contraseña cumpla con los requisitos de complejidad:
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un carácter especial (!@#$%^&*()_+-=[]{}|;:,.<>?)
    - Sin espacios
    - Sin emojis
    """

    def validate(self, password, user=None):
        """Valida la contraseña según los criterios de complejidad."""
        errors = []

        # Verificar mayúscula
        if not re.search(r'[A-Z]', password):
            errors.append(
                'La contraseña debe contener al menos una letra mayúscula.'
            )

        # Verificar minúscula
        if not re.search(r'[a-z]', password):
            errors.append(
                'La contraseña debe contener al menos una letra minúscula.'
            )

        # Verificar carácter especial
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            errors.append(
                'La contraseña debe contener al menos un carácter especial '
                '(!@#$%^&*()_+-=[]{}|;:,.<>?).'
            )

        # Verificar espacios
        if ' ' in password:
            errors.append('La contraseña no debe contener espacios.')

        # Verificar emojis (caracteres Unicode fuera del rango ASCII)
        if any(ord(char) > 127 for char in password):
            errors.append('La contraseña no debe contener emojis.')

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        """Retorna el texto de ayuda para el validador."""
        return _(
            'Tu contraseña debe contener al menos una letra mayúscula, '
            'una minúscula, un carácter especial y no debe contener espacios '
            'ni emojis.'
        )