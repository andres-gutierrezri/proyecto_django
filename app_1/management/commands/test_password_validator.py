#!/usr/bin/env python
"""
Script para probar el validador de contraseñas.
Ejecutar con: python3 test_password_validator.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

print("=" * 60)
print("PRUEBAS DEL VALIDADOR DE CONTRASEÑAS")
print("=" * 60)
print()

# Lista de pruebas
tests = [
    # (contraseña, debe_pasar, descripción)
    ("password", False, "Sin mayúscula y sin carácter especial"),
    ("PASSWORD", False, "Sin minúscula y sin carácter especial"),
    ("Password", False, "Sin carácter especial"),
    ("Password123", False, "Sin carácter especial"),
    ("password123!", False, "Sin mayúscula"),
    ("PASSWORD123!", False, "Sin minúscula"),
    ("Pass 123!", False, "Con espacios"),
    ("Pass123!😀", False, "Con emoji"),
    ("Abc1!", False, "Menos de 8 caracteres"),
    ("Password123!ExtraLong", False, "Más de 20 caracteres (22)"),
    ("Password123!ExtraLongPassword", False, "Más de 20 caracteres (30)"),
    ("Pass123!", True, "Válida - 8 caracteres exactos"),
    ("Password123!", True, "Válida - con todos los requisitos"),
    ("MyP@ssw0rd", True, "Válida - con símbolos alternativos"),
    ("Secure#2025", True, "Válida - formato corto"),
    ("MyC0mpl3x.Pass!", True, "Válida - formato largo (15 caracteres)"),
    ("Ab1!Cd2@Ef3#Gh4$Ij", True, "Válida - 20 caracteres exactos"),
]

passed = 0
failed = 0

for password, should_pass, description in tests:
    try:
        validate_password(password)
        result = "ACEPTADA"
        if should_pass:
            print(f"✅ {description}")
            print(f"   Contraseña: '{password}' - {result} (correcto)")
            passed += 1
        else:
            print(f"❌ {description}")
            print(f"   Contraseña: '{password}' - {result} (ERROR: debió rechazarse)")
            failed += 1
    except ValidationError as e:
        result = "RECHAZADA"
        if not should_pass:
            print(f"✅ {description}")
            print(f"   Contraseña: '{password}' - {result} (correcto)")
            print(f"   Errores: {', '.join(e.messages)}")
            passed += 1
        else:
            print(f"❌ {description}")
            print(f"   Contraseña: '{password}' - {result} (ERROR: debió aceptarse)")
            print(f"   Errores: {', '.join(e.messages)}")
            failed += 1
    print()

print("=" * 60)
print("RESUMEN DE PRUEBAS")
print("=" * 60)
print(f"Total de pruebas: {len(tests)}")
print(f"✅ Pruebas exitosas: {passed}")
print(f"❌ Pruebas fallidas: {failed}")
print()

if failed == 0:
    print("🎉 ¡Todos los validadores funcionan correctamente!")
else:
    print("⚠️  Hay validadores que necesitan revisión.")
    sys.exit(1)
