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
import glob
import re
from pathlib import Path

def setup_mysql_library_path():
    """Configura todas las variables de entorno necesarias para MySQL"""
    print("🔍 Detectando y configurando bibliotecas de MySQL...")
    
    if sys.platform == 'darwin':  # macOS
        # Buscar instalación de MySQL en ubicaciones comunes
        mysql_base_paths = [
            "/usr/local/mysql",
            "/opt/homebrew/opt/mysql",
            "/usr/local/opt/mysql",
        ]
        
        # Agregar rutas con comodines (Cellar de Homebrew)
        mysql_base_paths.extend(glob.glob("/opt/homebrew/Cellar/mysql/*"))
        mysql_base_paths.extend(glob.glob("/usr/local/Cellar/mysql/*"))
        
        mysql_root = None
        for path in mysql_base_paths:
            lib_path = Path(path) / "lib"
            if lib_path.exists():
                # Verificar que contenga la biblioteca
                if (lib_path / "libmysqlclient.dylib").exists() or \
                   (lib_path / "libmysqlclient.24.dylib").exists():
                    mysql_root = path
                    break
        
        if mysql_root:
            # Configurar todas las variables de entorno necesarias para MySQL
            mysql_bin = f"{mysql_root}/bin"
            mysql_lib = f"{mysql_root}/lib"
            mysql_include = f"{mysql_root}/include"
            mysql_pkgconfig = f"{mysql_root}/lib/pkgconfig"
            
            # PATH
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = f"{mysql_bin}:{current_path}"
            
            # MYSQLCLIENT_CFLAGS
            os.environ['MYSQLCLIENT_CFLAGS'] = f"-I{mysql_include}"
            
            # MYSQLCLIENT_LDFLAGS
            os.environ['MYSQLCLIENT_LDFLAGS'] = f"-L{mysql_lib} -lmysqlclient"
            
            # PKG_CONFIG_PATH
            os.environ['PKG_CONFIG_PATH'] = mysql_pkgconfig
            
            # DYLD_LIBRARY_PATH
            current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
            os.environ['DYLD_LIBRARY_PATH'] = f"{mysql_lib}:{current_dyld}" if current_dyld else mysql_lib
            
            # DYLD_FALLBACK_LIBRARY_PATH
            current_fallback = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')
            os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = f"{mysql_lib}:{current_fallback}" if current_fallback else mysql_lib
            
            print(f"✅ MySQL encontrado en: {mysql_root}")
            print("   Variables de entorno configuradas:")
            print("   - PATH")
            print("   - MYSQLCLIENT_CFLAGS")
            print("   - MYSQLCLIENT_LDFLAGS")
            print("   - PKG_CONFIG_PATH")
            print("   - DYLD_LIBRARY_PATH")
            print("   - DYLD_FALLBACK_LIBRARY_PATH")
            return True
        else:
            print("⚠️  No se encontraron bibliotecas de MySQL en ubicaciones estándar")
            print("   Si usas MySQL, asegúrate de tener MySQL instalado correctamente")
            print("   Puedes instalar MySQL con: brew install mysql")
            print()
            print("   O agregar estas variables a tu ~/.zprofile:")
            print('   export PATH="/usr/local/mysql/bin:$PATH"')
            print('   export MYSQLCLIENT_CFLAGS="-I/usr/local/mysql/include"')
            print('   export MYSQLCLIENT_LDFLAGS="-L/usr/local/mysql/lib -lmysqlclient"')
            print('   export PKG_CONFIG_PATH="/usr/local/mysql/lib/pkgconfig"')
            print('   export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_LIBRARY_PATH"')
            print('   export DYLD_FALLBACK_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_FALLBACK_LIBRARY_PATH"')
            return False
    
    elif sys.platform == 'win32':  # Windows
        # Buscar instalación de MySQL en ubicaciones comunes
        mysql_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\lib",
            r"C:\Program Files\MySQL\MySQL Server 8.4\lib",
            r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\lib",
            r"C:\MySQL\lib",
            r"C:\xampp\mysql\lib",
        ]
        
        mysql_lib_path = None
        for path in mysql_paths:
            if Path(path).exists() and (Path(path) / "libmysql.dll").exists():
                mysql_lib_path = path
                break
        
        if mysql_lib_path:
            # Agregar al PATH
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = f"{mysql_lib_path};{current_path}"
            print(f"✅ Bibliotecas de MySQL encontradas en: {mysql_lib_path}")
            print("   PATH actualizado")
            return True
        else:
            print("⚠️  No se encontraron bibliotecas de MySQL en ubicaciones estándar")
            print("   Si usas MySQL, asegúrate de tener MySQL instalado correctamente")
            return False
    
    return True  # En otros sistemas, no hacer nada

def create_virtual_environment():
    """Crea un entorno virtual si no existe"""
    venv_path = Path(__file__).parent / ".venv"
    
    if venv_path.exists():
        print("✅ Entorno virtual ya existe")
    else:
        print("🔨 Creando entorno virtual...")
        try:
            venv.create(venv_path, with_pip=True)
            print("✅ Entorno virtual creado exitosamente")
        except Exception as e:
            print(f"❌ Error al crear entorno virtual: {e}")
            sys.exit(1)
    
    # Mostrar información del entorno virtual
    print("\n📍 Información del entorno virtual:")
    print(f"   Ruta: {venv_path.absolute()}")
    
    if sys.platform == 'win32':
        activate_path = venv_path / "Scripts" / "activate.bat"
        python_path = venv_path / "Scripts" / "python.exe"
        print(f"   Activación manual: {activate_path}")
    else:
        activate_path = venv_path / "bin" / "activate"
        python_path = venv_path / "bin" / "python"
        print(f"   Activación manual: source {activate_path}")
    
    print(f"   Python: {python_path}")
    print()
    
    return venv_path

def recreate_virtual_environment():
    """Elimina y recrea el entorno virtual"""
    venv_path = Path(__file__).parent / ".venv"
    
    if venv_path.exists():
        print("🗑️  Eliminando entorno virtual corrupto...")
        try:
            shutil.rmtree(venv_path)
            print("✅ Entorno virtual eliminado")
        except Exception as e:
            print(f"⚠️  Error al eliminar entorno virtual: {e}")
    
    print("🔄 Recreando entorno virtual...")
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

def purge_pip_cache(python_executable):
    """Limpia el caché de pip"""
    print("🧹 Limpiando caché de pip...")
    try:
        subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "cache", 
            "purge"
        ], check=True, capture_output=True, text=True)
        print("✅ Caché de pip limpiado exitosamente")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  No se pudo limpiar el caché de pip (puede ser normal)")
        return False

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
    
    # Intentar instalación sin caché desde el principio
    print("📋 Instalando desde requirements.txt (sin caché)...")
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
        print("✅ Dependencias instaladas exitosamente")
        if result.stdout:
            # Mostrar solo las líneas importantes del output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Successfully installed' in line:
                    print(f"   {line}")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Error en instalación, intentando con reinstalación forzada...")
        
        # Intentar con reinstalación forzada
        try:
            result = subprocess.run([
                str(python_executable), 
                "-m", 
                "pip", 
                "install", 
                "--no-cache-dir",
                "--force-reinstall",
                "-r", 
                str(requirements_file)
            ], check=True, capture_output=True, text=True)
            print("✅ Dependencias instaladas exitosamente (con reinstalación forzada)")
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

def list_installed_packages(python_executable):
    """Lista los paquetes instalados en el entorno virtual"""
    print()
    print("📦 Paquetes instalados en el entorno virtual:")
    print("=" * 64)
    try:
        result = subprocess.run([
            str(python_executable), 
            "-m", 
            "pip", 
            "list", 
            "--format=columns"
        ], check=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        print("=" * 64)
    except subprocess.CalledProcessError:
        print("⚠️  No se pudo obtener la lista de paquetes")
        print("=" * 64)
    print()

def verify_mysqldb_import(python_executable):
    """Verifica que MySQLdb se pueda importar correctamente"""
    print("🔍 Verificando importación de MySQLdb...")
    try:
        result = subprocess.run([
            str(python_executable), 
            "-c", 
            "import MySQLdb; print('MySQLdb import successful')"
        ], check=True, capture_output=True, text=True)
        print("✅ MySQLdb importado exitosamente")
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print("⚠️  Advertencia: MySQLdb no pudo ser importado")
        print()
        print("💡 Soluciones posibles:")
        
        if sys.platform == 'darwin':  # macOS
            print("   1. Instalar MySQL:")
            print("      brew install mysql")
            print()
            print("   2. Agregar variables de entorno de MySQL a ~/.zprofile:")
            print('      export PATH="/usr/local/mysql/bin:$PATH"')
            print('      export MYSQLCLIENT_CFLAGS="-I/usr/local/mysql/include"')
            print('      export MYSQLCLIENT_LDFLAGS="-L/usr/local/mysql/lib -lmysqlclient"')
            print('      export PKG_CONFIG_PATH="/usr/local/mysql/lib/pkgconfig"')
            print('      export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_LIBRARY_PATH"')
            print('      export DYLD_FALLBACK_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_FALLBACK_LIBRARY_PATH"')
            print()
            print("   3. Reinstalar mysqlclient con las variables configuradas:")
            print("      source .venv/bin/activate")
            print("      pip uninstall mysqlclient -y")
            print("      pip install mysqlclient --no-cache-dir")
            print()
            print("   4. Si no usas MySQL, puedes cambiar a SQLite en settings.py")
            print()
            
            # Intentar detectar MySQL
            try:
                mysql_config = subprocess.run(['which', 'mysql_config'], 
                                            capture_output=True, text=True, check=True)
                if mysql_config.stdout.strip():
                    mysql_libs = subprocess.run(['mysql_config', '--libs'],
                                              capture_output=True, text=True, check=True)
                    if mysql_libs.stdout:
                        lib_paths = re.findall(r'-L(\S+)', mysql_libs.stdout)
                        if lib_paths:
                            mysql_base = str(Path(lib_paths[0]).parent)
                            print(f"   📌 MySQL detectado en: {mysql_base}")
                            print("   Asegúrate de tener todas las variables en tu ~/.zprofile")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("   ⚠️  MySQL no parece estar instalado en el sistema")
        
        elif sys.platform == 'win32':  # Windows
            print("   1. Instalar MySQL Server desde: https://dev.mysql.com/downloads/mysql/")
            print()
            print("   2. Agregar MySQL al PATH del sistema")
            print("      Ejemplo: C:\\Program Files\\MySQL\\MySQL Server 8.0\\lib")
            print()
            print("   3. Reinstalar mysqlclient en el entorno virtual:")
            print("      .venv\\Scripts\\activate")
            print("      pip uninstall mysqlclient -y")
            print("      pip install mysqlclient --no-cache-dir")
            print()
            print("   4. Si no usas MySQL, puedes cambiar a SQLite en settings.py")
        
        print()
        if e.stderr:
            print(f"   Detalle del error: {e.stderr.strip()}")
        
        return False

def create_default_superuser(python_executable):
    """Crea el superusuario por defecto si no existe"""
    print("👤 Creando superusuario por defecto (si no existe)...")
    try:
        result = subprocess.run([
            str(python_executable),
            "create_default_superuser.py"
        ], cwd=Path(__file__).parent, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia al crear superusuario (puede ser normal si ya existe)")
        if e.stderr:
            print(f"Advertencia: {e.stderr}")
        # No hacer sys.exit(1) aquí porque puede fallar si ya existe

def run_migrations(python_executable):
    """Ejecuta las migraciones de Django"""
    # Primero recolectar archivos estáticos
    print("📁 Recolectando archivos estáticos...")
    try:
        result = subprocess.run([
            str(python_executable),
            "manage.py",
            "collectstatic",
            "--noinput"
        ], cwd=Path(__file__).parent, check=True, capture_output=True, text=True)
        print("✅ Archivos estáticos recolectados exitosamente")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia al recolectar archivos estáticos (puede ser normal si no está configurado)")
        if e.stderr:
            print(f"Advertencia: {e.stderr}")
        # No hacer sys.exit(1) aquí porque collectstatic puede fallar si no está configurado

    # Después ejecutar makemigrations
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

    # Finalmente crear superusuario
    create_default_superuser(python_executable)

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
        print("================================================================")
        print("👋 Gracias por usar el iniciador de aplicación Django")
        print("================================================================")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("=" * 60)
    print("🐍 INICIADOR DE APLICACIÓN DJANGO CON ENTORNO VIRTUAL")
    print("=" * 60)
    
    # Paso 0: Configurar bibliotecas de MySQL
    setup_mysql_library_path()
    
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
        
        # Paso 2.5: Limpiar caché de pip
        purge_pip_cache(python_executable)
        
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
        
        # Paso 3.5: Listar paquetes instalados
        list_installed_packages(python_executable)
        
        # Paso 4: Ejecutar migraciones
        run_migrations(python_executable)
        
        # Paso 4.5: Verificar importación de MySQLdb
        verify_mysqldb_import(python_executable)
        
        # Paso 5: Iniciar servidor
        start_server(python_executable)
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()