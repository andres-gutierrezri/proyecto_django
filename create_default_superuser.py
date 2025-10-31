#!/usr/bin/env python
"""
Script para crear un superusuario por defecto automáticamente.
Se ejecuta al iniciar el servidor usando variables de entorno.

Este script configura el entorno de Django e inicializa la aplicación
para poder interactuar con el modelo de usuario.

Variables de entorno requeridas:
- DJANGO_SUPERUSER_EMAIL: Email del superusuario
- DJANGO_SUPERUSER_USERNAME: Username del superusuario
- DJANGO_SUPERUSER_PASSWORD: Contraseña del superusuario
- DJANGO_SUPERUSER_FIRST_NAME: Nombre (opcional, default: Admin)
- DJANGO_SUPERUSER_LAST_NAME: Apellido (opcional, default: User)
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path de Python
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

# Inicializar Django
django.setup()

# Importar el modelo de usuario después de configurar Django
from django.contrib.auth import get_user_model


def create_superuser():
    """Crea un superusuario por defecto si no existe."""
    User = get_user_model()

    # Obtener credenciales desde variables de entorno
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
    last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME', 'User')

    # Validar que existan las credenciales
    if not email or not username or not password:
        print('⚠️  Variables de entorno del superusuario no configuradas.')
        print('   Saltando creación automática.')
        print('   Configure: DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_USERNAME, '
              'DJANGO_SUPERUSER_PASSWORD')
        return False

    # Verificar si el superusuario ya existe (por email o username)
    if User.objects.filter(email=email).exists():
        print(f'⚠️  Superusuario con email "{email}" ya existe. Saltando creación.')
        return False

    if User.objects.filter(username=username).exists():
        print(f'⚠️  Superusuario con username "{username}" ya existe. Saltando creación.')
        return False

    # Crear el superusuario
    try:
        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.email_verified = True  # Marcar email como verificado
        user.terms_accepted = True  # Aceptar términos automáticamente
        user.save()

        print('✅ Superusuario creado exitosamente:')
        print(f'   Email: {email}')
        print(f'   Username: {username}')
        print(f'   Nombre: {first_name} {last_name}')
        print('   Puede iniciar sesión en /admin/ con estas credenciales')
        return True

    except Exception as e:
        print(f'❌ Error al crear superusuario: {e}')
        return False


if __name__ == '__main__':
    try:
        create_superuser()
    except Exception as e:
        print(f'❌ Error fatal al ejecutar script: {e}')
        sys.exit(1)