"""
Script de prueba para verificar la contraseña de un usuario.
Uso: python test_password.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from django.contrib.auth import get_user_model
from getpass import getpass

User = get_user_model()

def test_password():
    print("=" * 60)
    print("PRUEBA DE VERIFICACIÓN DE CONTRASEÑA")
    print("=" * 60)
    
    # Pedir email
    email = input("\nIngresa el email del usuario: ").strip()
    
    try:
        user = User.objects.get(email=email)
        print(f"\n✓ Usuario encontrado: {user.get_full_name()} ({user.email})")
    except User.DoesNotExist:
        print(f"\n✗ Error: No existe un usuario con email '{email}'")
        return
    
    # Pedir contraseña
    password = getpass("\nIngresa la contraseña a verificar: ")
    
    # Información de debug
    print(f"\n{'─' * 60}")
    print("INFORMACIÓN DE DEBUG:")
    print(f"{'─' * 60}")
    print(f"Longitud de contraseña ingresada: {len(password)}")
    print(f"Tiene espacios al inicio: {password != password.lstrip()}")
    print(f"Tiene espacios al final: {password != password.rstrip()}")
    print(f"Longitud después de strip: {len(password.strip())}")
    
    # Verificar contraseña original
    is_valid_original = user.check_password(password)
    print(f"\n{'─' * 60}")
    print("RESULTADO CONTRASEÑA ORIGINAL:")
    print(f"{'─' * 60}")
    print(f"✓ VÁLIDA" if is_valid_original else "✗ INVÁLIDA")
    
    # Verificar contraseña con strip
    password_stripped = password.strip()
    is_valid_stripped = user.check_password(password_stripped)
    print(f"\n{'─' * 60}")
    print("RESULTADO CONTRASEÑA CON STRIP:")
    print(f"{'─' * 60}")
    print(f"✓ VÁLIDA" if is_valid_stripped else "✗ INVÁLIDA")
    
    # Resultado final
    print(f"\n{'=' * 60}")
    if is_valid_original or is_valid_stripped:
        print("✅ CONTRASEÑA CORRECTA")
        if not is_valid_original and is_valid_stripped:
            print("⚠️  NOTA: La contraseña tiene espacios al inicio o final")
    else:
        print("❌ CONTRASEÑA INCORRECTA")
        print("\nPosibles causas:")
        print("  • La contraseña ingresada no coincide")
        print("  • Hay caracteres especiales o encoding diferente")
        print("  • La contraseña en la BD está corrupta")
    print(f"{'=' * 60}\n")

if __name__ == '__main__':
    test_password()
