#!/usr/bin/env python
"""
Script para iniciar la aplicación Django
- Crea y activa entorno virtual
- Actualiza pip
- Instala dependencias
- Ejecuta las migraciones
- Inicia el servidor de desarrollo
- Abre el navegador en la URL de la aplicación
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import venv
from pathlib import Path

def create_virtual_environment():
    """Crea un entorno virtual si no existe"""
    venv_path = Path(__file__).parent / ".venv"
    
    if venv_path.exists():
        print("✅ Entorno virtual ya existe")
        return venv_path
    
    print("🔨 Creando entorno virtual...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Entorno virtual creado exitosamente")
        return venv_path
    except Exception as e:
        print(f"❌ Error al crear entorno virtual: {e}")
        sys.exit(1)

def get_venv_python(venv_path):
    """Obtiene la ruta del ejecutable de Python del entorno virtual"""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "python"

def upgrade_pip(python_executable):
    """Actualiza pip en el entorno virtual"""
    print("⬆️  Actualizando pip...")
    try:
        result = subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "install", 
            "--upgrade", 
            "pip"
        ], check=True, capture_output=True, text=True)
        print("✅ Pip actualizado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia al actualizar pip: {e}")
        return False

def install_requirements(python_executable):
    """Instala las dependencias del archivo requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("⚠️  No se encontró requirements.txt, continuando sin instalar dependencias...")
        return True
    
    print("📦 Instalando dependencias desde requirements.txt...")
    try:
        result = subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            str(requirements_file)
        ], check=True, capture_output=True, text=True)
        print("✅ Dependencias instaladas exitosamente")
        if result.stdout:
            # Mostrar solo las líneas importantes del output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Successfully installed' in line:
                    print(f"   {line}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def run_migrations(python_executable):
    """Ejecuta las migraciones de Django"""
    print("🔄 Ejecutando migraciones...")
    try:
        result = subprocess.run([
            str(python_executable), 
            "manage.py", 
            "migrate"
        ], cwd=Path(__file__).parent, check=True, capture_output=True, text=True)
        print("✅ Migraciones completadas exitosamente")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar migraciones: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)

def open_browser_delayed():
    """Abre el navegador después de un pequeño delay para que el servidor esté listo"""
    time.sleep(3)  # Espera 3 segundos para que el servidor esté completamente iniciado
    url = "http://127.0.0.1:8000/app_1/"
    print(f"🌐 Abriendo navegador en: {url}")
    webbrowser.open(url)

def start_server(python_executable):
    """Inicia el servidor de desarrollo de Django"""
    print("🚀 Iniciando servidor de desarrollo...")
    print("📍 URL de la aplicación: http://127.0.0.1:8000/app_1/")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    
    # Iniciar hilo para abrir el navegador
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Ejecutar el servidor
        subprocess.run([
            str(python_executable), 
            "manage.py", 
            "runserver", 
            "127.0.0.1:8000"
        ], cwd=Path(__file__).parent, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("=" * 60)
    print("🐍 INICIADOR DE APLICACIÓN DJANGO CON ENTORNO VIRTUAL")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent
    manage_py = project_root / "manage.py"
    
    if not manage_py.exists():
        print(f"❌ Error: No se encontró manage.py en {project_root}")
        print("   Asegúrate de que el script esté en la carpeta raíz del proyecto Django")
        sys.exit(1)
    
    try:
        # Paso 1: Crear/verificar entorno virtual
        venv_path = create_virtual_environment()
        python_executable = get_venv_python(venv_path)
        
        if not python_executable.exists():
            print(f"❌ Error: No se encontró el ejecutable de Python en {python_executable}")
            sys.exit(1)
        
        print(f"🐍 Usando Python del entorno virtual: {python_executable}")
        
        # Paso 2: Actualizar pip
        upgrade_pip(python_executable)
        
        # Paso 3: Instalar dependencias
        if not install_requirements(python_executable):
            print("❌ Error al instalar dependencias")
            sys.exit(1)
        
        # Paso 4: Ejecutar migraciones
        run_migrations(python_executable)
        
        # Paso 5: Iniciar servidor
        start_server(python_executable)
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
