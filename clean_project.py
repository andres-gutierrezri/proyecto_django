#!/usr/bin/env python3
"""
================================================================
SCRIPT DE LIMPIEZA COMPLETA DEL PROYECTO DJANGO
================================================================
Este script realiza las siguientes tareas:
1. Elimina todas las migraciones del proyecto
2. Elimina y recrea la base de datos MySQL
3. Elimina el entorno virtual de Python
================================================================
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


class Colors:
    """Códigos ANSI para colores en la terminal."""
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # Sin color


def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Imprime un encabezado con formato."""
    print()
    print(f"{Colors.MAGENTA}{'=' * 64}{Colors.NC}")
    print(f"{Colors.MAGENTA}{title}{Colors.NC}")
    print(f"{Colors.MAGENTA}{'=' * 64}{Colors.NC}")
    print()


def print_menu():
    """Muestra el menú principal."""
    print("=" * 64)
    print("LIMPIEZA COMPLETA DEL PROYECTO DJANGO")
    print("=" * 64)
    print()
    print(f"{Colors.CYAN}Seleccione las tareas a realizar:{Colors.NC}")
    print()
    print(f"{Colors.YELLOW}1){Colors.NC} Eliminar migraciones")
    print(f"{Colors.YELLOW}2){Colors.NC} Eliminar y recrear base de datos MySQL")
    print(f"{Colors.YELLOW}3){Colors.NC} Eliminar entorno virtual de Python")
    print(f"{Colors.YELLOW}4){Colors.NC} Ejecutar todas las tareas (1 + 2 + 3)")
    print(f"{Colors.YELLOW}5){Colors.NC} Salir")
    print()


def delete_migrations():
    """
    Elimina todos los archivos de migraciones del proyecto.
    
    Returns:
        bool: True si se ejecutó correctamente
    """
    print_header("TAREA 1: ELIMINAR MIGRACIONES")
    
    project_root = Path.cwd()
    py_files = []
    pyc_files = []
    
    print(f"{Colors.YELLOW}🔍 Buscando archivos de migraciones...{Colors.NC}")
    print()
    
    # Buscar archivos de migraciones
    for root, dirs, files in os.walk(project_root):
        if 'migrations' in Path(root).parts:
            for file in files:
                file_path = Path(root) / file
                
                if file.endswith('.py') and file != '__init__.py':
                    py_files.append(file_path)
                elif file.endswith('.pyc'):
                    pyc_files.append(file_path)
    
    # Mostrar estadísticas
    print(f"{Colors.BLUE}📊 Archivos encontrados:{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Archivos .py de migraciones: {Colors.YELLOW}{len(py_files)}{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Archivos .pyc compilados: {Colors.YELLOW}{len(pyc_files)}{Colors.NC}")
    print()
    
    if len(py_files) == 0 and len(pyc_files) == 0:
        print(f"{Colors.GREEN}✅ No hay archivos de migraciones para eliminar.{Colors.NC}")
        return True
    
    # Pedir confirmación antes de eliminar
    print(f"{Colors.YELLOW}⚠️  Se encontraron archivos de migraciones para eliminar.{Colors.NC}")
    print()
    response = input(f"{Colors.YELLOW}¿Desea continuar con la eliminación? (s/n): {Colors.NC}").strip().lower()
    if response not in ['s', 'si', 'sí', 'y', 'yes']:
        print(f"{Colors.YELLOW}❌ Operación cancelada.{Colors.NC}")
        return True
    print()
    
    # Eliminar archivos
    deleted_py = 0
    deleted_pyc = 0
    
    if py_files:
        print(f"{Colors.YELLOW}→{Colors.NC} Eliminando archivos .py...")
        for file_path in py_files:
            try:
                file_path.unlink()
                deleted_py += 1
            except Exception as e:
                print(f"{Colors.RED}❌ Error al eliminar {file_path}: {e}{Colors.NC}")
        print(f"{Colors.GREEN}✅ {deleted_py} archivos .py eliminados{Colors.NC}")
    
    if pyc_files:
        print(f"{Colors.YELLOW}→{Colors.NC} Eliminando archivos .pyc...")
        for file_path in pyc_files:
            try:
                file_path.unlink()
                deleted_pyc += 1
            except Exception as e:
                print(f"{Colors.RED}❌ Error al eliminar {file_path}: {e}{Colors.NC}")
        print(f"{Colors.GREEN}✅ {deleted_pyc} archivos .pyc eliminados{Colors.NC}")
    
    print()
    print(f"{Colors.GREEN}✅ Migraciones eliminadas exitosamente.{Colors.NC}")
    return True


def load_env_variables():
    """
    Carga las variables de entorno desde el archivo .env
    
    Returns:
        dict: Diccionario con las variables de entorno o None si hay error
    """
    env_file = Path('.env')
    
    if not env_file.exists():
        print(f"{Colors.RED}❌ Error: No se encontró el archivo .env{Colors.NC}")
        return None
    
    env_vars = {}
    
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith('#'):
                continue
            
            # Separar clave y valor
            if '=' in line:
                key, value = line.split('=', 1)
                # Eliminar comillas simples y dobles
                value = value.strip().strip("'\"")
                env_vars[key.strip()] = value
    
    return env_vars


def recreate_database():
    """
    Elimina y recrea la base de datos MySQL.
    
    Returns:
        bool: True si se ejecutó correctamente
    """
    print_header("TAREA 2: RECREAR BASE DE DATOS MYSQL")
    
    print(f"{Colors.BLUE}📁 Cargando variables de entorno desde .env...{Colors.NC}")
    env_vars = load_env_variables()
    
    if not env_vars:
        return False
    
    # Validar variables necesarias
    required_vars = ['MYSQL_DB_NAME', 'MYSQL_DB_USER', 'MYSQL_DB_PASSWORD', 
                     'MYSQL_DB_HOST', 'MYSQL_DB_PORT']
    
    missing_vars = [var for var in required_vars if var not in env_vars or not env_vars[var]]
    
    if missing_vars:
        print(f"{Colors.RED}❌ Error: Faltan variables de entorno necesarias en .env{Colors.NC}")
        print(f"{Colors.YELLOW}   Variables faltantes: {', '.join(missing_vars)}{Colors.NC}")
        return False
    
    print(f"{Colors.GREEN}✅ Variables de entorno cargadas correctamente{Colors.NC}")
    print()
    print(f"{Colors.BLUE}📊 Configuración de la base de datos:{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Nombre: {Colors.YELLOW}{env_vars['MYSQL_DB_NAME']}{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Usuario: {Colors.YELLOW}{env_vars['MYSQL_DB_USER']}{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Host: {Colors.YELLOW}{env_vars['MYSQL_DB_HOST']}{Colors.NC}")
    print(f"   {Colors.YELLOW}→{Colors.NC} Puerto: {Colors.YELLOW}{env_vars['MYSQL_DB_PORT']}{Colors.NC}")
    print()
    
    # Función auxiliar para ejecutar comandos MySQL
    def execute_mysql(sql_command, capture_output=False):
        cmd = [
            'mysql',
            f"-u{env_vars['MYSQL_DB_USER']}",
            f"-p{env_vars['MYSQL_DB_PASSWORD']}",
            f"-h{env_vars['MYSQL_DB_HOST']}",
            f"-P{env_vars['MYSQL_DB_PORT']}",
            '-e',
            sql_command
        ]
        
        try:
            if capture_output:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                return result.stdout.strip()
            else:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
                return True
        except subprocess.CalledProcessError:
            return False if not capture_output else ""
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Error: MySQL no está instalado o no está en el PATH{Colors.NC}")
            return False if not capture_output else ""
    
    # Verificar si la base de datos existe
    print(f"{Colors.YELLOW}🔍 Verificando existencia de la base de datos...{Colors.NC}")
    check_sql = f"SHOW DATABASES LIKE '{env_vars['MYSQL_DB_NAME']}';"
    db_exists = execute_mysql(check_sql, capture_output=True)
    
    if db_exists:
        print(f"{Colors.GREEN}✅ Base de datos '{env_vars['MYSQL_DB_NAME']}' encontrada{Colors.NC}")
    else:
        print(f"{Colors.YELLOW}⚠️  La base de datos '{env_vars['MYSQL_DB_NAME']}' no existe{Colors.NC}")
        print(f"{Colors.BLUE}ℹ️  Se creará una nueva base de datos{Colors.NC}")
    
    print()
    
    # Eliminar base de datos si existe
    if db_exists:
        print(f"{Colors.YELLOW}🗑️  Eliminando base de datos existente...{Colors.NC}")
        drop_sql = f"DROP DATABASE IF EXISTS `{env_vars['MYSQL_DB_NAME']}`;"
    # Eliminar base de datos si existe
    if db_exists:
        print(f"{Colors.YELLOW}🗑️  Eliminando base de datos existente...{Colors.NC}")
        drop_sql = f"DROP DATABASE IF EXISTS `{env_vars['MYSQL_DB_NAME']}`;"
        
        if execute_mysql(drop_sql):
            print(f"{Colors.GREEN}✅ Base de datos eliminada exitosamente{Colors.NC}")
        else:
            print(f"{Colors.RED}❌ Error al eliminar la base de datos{Colors.NC}")
            return False
    
    print()
    
    # Crear base de datos
    print(f"{Colors.YELLOW}🔨 Creando nueva base de datos...{Colors.NC}")
    create_sql = f"CREATE DATABASE `{env_vars['MYSQL_DB_NAME']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    if execute_mysql(create_sql):
        print(f"{Colors.GREEN}✅ Base de datos creada exitosamente{Colors.NC}")
    else:
        print(f"{Colors.RED}❌ Error al crear la base de datos{Colors.NC}")
        return False
    
    print()
    print(f"{Colors.GREEN}✅ Base de datos '{env_vars['MYSQL_DB_NAME']}' recreada exitosamente.{Colors.NC}")
    return True


def delete_virtualenv():
    """
    Elimina el entorno virtual de Python.
    
    Returns:
        bool: True si se ejecutó correctamente
    """
    print_header("TAREA 3: ELIMINAR ENTORNO VIRTUAL")
    
    venv_path = Path('.venv')
    
    if not venv_path.exists():
        print(f"{Colors.YELLOW}⚠️  El entorno virtual no existe (.venv){Colors.NC}")
        return True
    
    print(f"{Colors.YELLOW}🗑️  Eliminando entorno virtual...{Colors.NC}")
    
    try:
        shutil.rmtree(venv_path)
        print(f"{Colors.GREEN}✅ Entorno virtual eliminado exitosamente{Colors.NC}")
        return True
    except Exception as e:
        print(f"{Colors.RED}❌ Error al eliminar el entorno virtual: {e}{Colors.NC}")
        return False


def show_final_instructions():
    """Muestra las instrucciones finales."""
    print()
    print(f"{Colors.CYAN}{'=' * 64}{Colors.NC}")
    print(f"{Colors.CYAN}INSTRUCCIONES PARA CONTINUAR{Colors.NC}")
    print(f"{Colors.CYAN}{'=' * 64}{Colors.NC}")
    print()
    print(f"{Colors.YELLOW}📝 Próximos pasos recomendados:{Colors.NC}")
    print()
    print(f"{Colors.BLUE}1. Recrear el entorno virtual:{Colors.NC}")
    print(f"   {Colors.YELLOW}python3 -m venv .venv{Colors.NC}")
    print(f"   {Colors.YELLOW}source .venv/bin/activate{Colors.NC}  # Linux/macOS")
    print(f"   {Colors.YELLOW}.venv\\Scripts\\activate{Colors.NC}      # Windows")
    print(f"   {Colors.YELLOW}pip install -r requirements.txt{Colors.NC}")
    print()
    print(f"{Colors.BLUE}2. Crear las migraciones:{Colors.NC}")
    print(f"   {Colors.YELLOW}python manage.py makemigrations{Colors.NC}")
    print(f"   {Colors.YELLOW}python manage.py migrate{Colors.NC}")
    print()
    print(f"{Colors.BLUE}3. Crear el superusuario:{Colors.NC}")
    print(f"   {Colors.YELLOW}python create_default_superuser.py{Colors.NC}")
    print()
    print(f"{Colors.CYAN}{'=' * 64}{Colors.NC}")


def confirm_action(message):
    """
    Solicita confirmación al usuario.
    
    Args:
        message: Mensaje a mostrar
        
    Returns:
        bool: True si el usuario confirma
    """
    print()
    print(message)
    response = input(f"{Colors.YELLOW}¿Desea continuar? (s/n): {Colors.NC}").strip().lower()
    return response in ['s', 'si', 'sí', 'y', 'yes']


def main():
    """Función principal del script."""
    while True:
        clear_screen()
        print_menu()
        
        try:
            opcion = input(f"{Colors.YELLOW}Seleccione una opción [1-5]: {Colors.NC}").strip()
            
            if opcion == '1':
                delete_migrations()
                
            elif opcion == '2':
                if confirm_action(
                    f"{Colors.RED}⚠️  ADVERTENCIA: Esta acción eliminará y recreará la base de datos.\n"
                    f"   TODOS los datos se perderán de forma permanente.{Colors.NC}"
                ):
                    recreate_database()
                else:
                    print(f"{Colors.YELLOW}❌ Operación cancelada.{Colors.NC}")
                    
            elif opcion == '3':
                if confirm_action(
                    f"{Colors.RED}⚠️  ADVERTENCIA: Esta acción eliminará el entorno virtual.{Colors.NC}"
                ):
                    delete_virtualenv()
                else:
                    print(f"{Colors.YELLOW}❌ Operación cancelada.{Colors.NC}")
                    
            elif opcion == '4':
                if confirm_action(
                    f"{Colors.RED}⚠️  ADVERTENCIA: Esta acción realizará las siguientes tareas:\n"
                    f"   1. Eliminar todas las migraciones\n"
                    f"   2. Eliminar y recrear la base de datos\n"
                    f"   3. Eliminar el entorno virtual\n"
                    f"   TODOS los datos se perderán de forma permanente.{Colors.NC}"
                ):
                    delete_migrations()
                    recreate_database()
                    delete_virtualenv()
                    show_final_instructions()
                else:
                    print(f"{Colors.YELLOW}❌ Operación cancelada.{Colors.NC}")
                    
            elif opcion == '5':
                print()
                print(f"{Colors.GREEN}👋 ¡Hasta luego!{Colors.NC}")
                print()
                return 0
                
            else:
                print(f"{Colors.RED}❌ Opción inválida. Por favor seleccione una opción del 1 al 5.{Colors.NC}")
            
            print()
            input(f"{Colors.CYAN}Presione ENTER para continuar...{Colors.NC}")
            
        except KeyboardInterrupt:
            print()
            print(f"{Colors.YELLOW}❌ Operación cancelada por el usuario (Ctrl+C).{Colors.NC}")
            print()
            return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print()
        print(f"{Colors.RED}❌ Error inesperado: {e}{Colors.NC}")
        print()
        sys.exit(1)
