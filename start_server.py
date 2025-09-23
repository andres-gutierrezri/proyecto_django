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
import urllib.request
import shutil
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

def recreate_virtual_environment():
    """Elimina y recrea el entorno virtual"""
    venv_path = Path(__file__).parent / ".venv"
    
    if venv_path.exists():
        print("🗑️  Eliminando entorno virtual corrupto...")
        import shutil
        try:
            shutil.rmtree(venv_path)
            print("✅ Entorno virtual eliminado")
        except Exception as e:
            print(f"⚠️  Error al eliminar entorno virtual: {e}")
    
    return create_virtual_environment()

def get_venv_python(venv_path):
    """Obtiene la ruta del ejecutable de Python del entorno virtual"""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        return venv_path / "bin" / "python"

def fix_and_upgrade_pip(python_executable):
    """Verifica, repara y actualiza pip en el entorno virtual"""
    print("🔧 Verificando y configurando pip...")
    
    # Primero verificar si pip funciona
    try:
        result = subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "--version"
        ], check=True, capture_output=True, text=True)
        print("✅ Pip está funcionando correctamente")
    except subprocess.CalledProcessError:
        print("🔧 Pip no funciona correctamente, intentando reparar...")
        
        # Intentar instalar pip usando ensurepip
        try:
            print("   Reinstalando pip con ensurepip...")
            subprocess.run([
                str(python_executable), 
                "-m", 
                "ensurepip", 
                "--upgrade"
            ], check=True, capture_output=True, text=True)
            print("✅ Pip reinstalado exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  No se pudo usar ensurepip: {e}")
            
            # Como último recurso, intentar con get-pip.py
            try:
                print("   Descargando e instalando pip manualmente...")
                import urllib.request
                get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
                get_pip_path = Path(__file__).parent / "get-pip.py"
                
                urllib.request.urlretrieve(get_pip_url, get_pip_path)
                subprocess.run([
                    str(python_executable), 
                    str(get_pip_path)
                ], check=True, capture_output=True, text=True)
                
                # Limpiar archivo temporal
                get_pip_path.unlink()
                print("✅ Pip instalado manualmente")
            except Exception as e:
                print(f"❌ Error al instalar pip manualmente: {e}")
                return False
    
    # Ahora intentar actualizar pip
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
        # Intentar con --force-reinstall
        try:
            print("   Intentando actualización forzada...")
            subprocess.run([
                str(python_executable), 
                "-m", 
                "pip", 
                "install", 
                "--upgrade", 
                "--force-reinstall", 
                "pip"
            ], check=True, capture_output=True, text=True)
            print("✅ Pip actualizado con reinstalación forzada")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  No se pudo actualizar pip, pero continuando...")
            return True

def install_requirements(python_executable):
    """Instala las dependencias del archivo requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("⚠️  No se encontró requirements.txt, continuando sin instalar dependencias...")
        return True
    
    print("📦 Instalando dependencias desde requirements.txt...")
    
    # Primero verificar que pip funciona
    try:
        subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "--version"
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("❌ Pip no está funcionando correctamente")
        return False
    
    # Intentar instalación normal
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
        print(f"⚠️  Error en instalación normal, intentando con --no-cache-dir...")
        
        # Intentar sin caché
        try:
            result = subprocess.run([
                str(python_executable), 
                "-m", 
                "pip", 
                "install", 
                "--no-cache-dir",
                "-r", 
                str(requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Dependencias instaladas exitosamente (sin caché)")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"❌ Error al instalar dependencias: {e2}")
            if e2.stderr:
                print(f"Error detallado: {e2.stderr}")
            
            # Mostrar sugerencias
            print("\n💡 Sugerencias para solucionar el problema:")
            print("   1. Verificar conexión a internet")
            print("   2. Ejecutar desde terminal: .venv\\Scripts\\activate && pip install --upgrade pip")
            print("   3. Instalar dependencias manualmente una por una")
            
            return False

def run_migrations(python_executable):
    """Ejecuta las migraciones de Django"""
    # Primero ejecutar makemigrations
    print("🔄 Ejecutando makemigrations...")
    try:
        result = subprocess.run([
            str(python_executable), 
            "manage.py", 
            "makemigrations"
        ], cwd=Path(__file__).parent, check=True, capture_output=True, text=True)
        print("✅ Makemigrations completado exitosamente")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia al ejecutar makemigrations: {e}")
        if e.stderr:
            print(f"Advertencia: {e.stderr}")
        # No hacer sys.exit(1) aquí porque makemigrations puede fallar si no hay cambios
    
    # Después ejecutar migrate
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
    url = "http://127.0.0.1:8000/"
    print(f"🌐 Abriendo navegador en: {url}")
    webbrowser.open(url)

def start_server(python_executable):
    """Inicia el servidor de desarrollo de Django"""
    print("🚀 Iniciando servidor de desarrollo...")
    print("📍 URL de la aplicación: http://127.0.0.1:8000/")
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
        
        # Paso 2: Verificar y configurar pip
        pip_success = fix_and_upgrade_pip(python_executable)
        
        if not pip_success:
            print("\n🔄 Intentando recrear el entorno virtual...")
            venv_path = recreate_virtual_environment()
            python_executable = get_venv_python(venv_path)
            
            if not fix_and_upgrade_pip(python_executable):
                print("❌ Error crítico con pip, no se puede continuar")
                print("\n💡 Soluciones manuales:")
                print("   1. Eliminar manualmente la carpeta .venv")
                print("   2. Verificar que Python esté correctamente instalado")
                print("   3. Ejecutar: python -m venv .venv")
                sys.exit(1)
        
        # Paso 3: Instalar dependencias
        if not install_requirements(python_executable):
            print("\n🔄 ¿Desea intentar recrear el entorno virtual? (s/n)")
            try:
                response = input().lower().strip()
                if response in ['s', 'si', 'sí', 'y', 'yes']:
                    print("🔄 Recreando entorno virtual...")
                    venv_path = recreate_virtual_environment()
                    python_executable = get_venv_python(venv_path)
                    
                    if fix_and_upgrade_pip(python_executable) and install_requirements(python_executable):
                        print("✅ Dependencias instaladas después de recrear entorno virtual")
                    else:
                        print("❌ Error persistente al instalar dependencias")
                        sys.exit(1)
                else:
                    print("❌ No se pudieron instalar las dependencias")
                    sys.exit(1)
            except (KeyboardInterrupt, EOFError):
                print("\n❌ Operación cancelada por el usuario")
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