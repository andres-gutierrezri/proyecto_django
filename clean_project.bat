@echo off
setlocal enabledelayedexpansion

REM ================================================================
REM SCRIPT DE LIMPIEZA COMPLETA DEL PROYECTO DJANGO
REM ================================================================
REM Este script realiza las siguientes tareas:
REM 1. Elimina todas las migraciones del proyecto
REM 2. Elimina y recrea la base de datos MySQL
REM 3. Elimina el entorno virtual de Python
REM ================================================================

:inicio
cls
echo ================================================================
echo LIMPIEZA COMPLETA DEL PROYECTO DJANGO
echo ================================================================
echo.

REM ================================================================
REM MENÚ PRINCIPAL
REM ================================================================
:menu
echo [96mSeleccione las tareas a realizar:[0m
echo.
echo [93m1)[0m Eliminar migraciones
echo [93m2)[0m Eliminar y recrear base de datos MySQL
echo [93m3)[0m Eliminar entorno virtual de Python
echo [93m4)[0m Ejecutar todas las tareas (1 + 2 + 3)
echo [93m5)[0m Salir
echo.
set /p opcion="[93mSeleccione una opcion [1-5]: [0m"

if "%opcion%"=="1" goto delete_migrations
if "%opcion%"=="2" goto confirm_database
if "%opcion%"=="3" goto confirm_virtualenv
if "%opcion%"=="4" goto confirm_all
if "%opcion%"=="5" goto salir
echo [91m❌ Opcion invalida. Por favor seleccione una opcion del 1 al 5.[0m
pause
goto inicio

REM ================================================================
REM FUNCIÓN: Eliminar migraciones
REM ================================================================
:delete_migrations
echo.
echo [95m================================================================[0m
echo [95mTAREA 1: ELIMINAR MIGRACIONES[0m
echo [95m================================================================[0m
echo.

set /a py_count=0
set /a pyc_count=0

echo [93m🔍 Buscando archivos de migraciones...[0m
echo.

REM Contar archivos .py de migraciones (excepto __init__.py)
for /r %%i in (migrations\*.py) do (
    echo %%~nxi | findstr /v /i "__init__.py" >nul
    if not errorlevel 1 (
        set /a py_count+=1
    )
)

REM Contar archivos .pyc
for /r %%i in (migrations\*.pyc) do (
    set /a pyc_count+=1
)

echo [94m📊 Archivos encontrados:[0m
echo    → Archivos .py de migraciones: %py_count%
echo    → Archivos .pyc compilados: %pyc_count%
echo.

if %py_count% equ 0 if %pyc_count% equ 0 (
    echo [92m✅ No hay archivos de migraciones para eliminar.[0m
    goto end_migrations
)

REM Pedir confirmación antes de eliminar
echo [93m⚠️  Se encontraron archivos de migraciones para eliminar.[0m
echo.
set /p confirmacion_mig="[93m¿Desea continuar con la eliminacion? (s/n): [0m"
if /i not "%confirmacion_mig%"=="s" (
    echo [93m❌ Operacion cancelada.[0m
    goto end_migrations
)
echo.

REM Eliminar archivos .py de migraciones (excepto __init__.py)
if %py_count% gtr 0 (
    echo → Eliminando archivos .py...
    for /r %%i in (migrations\*.py) do (
        echo %%~nxi | findstr /v /i "__init__.py" >nul
        if not errorlevel 1 (
            del /q "%%i"
        )
    )
    echo [92m✅ %py_count% archivos .py eliminados[0m
)

REM Eliminar archivos .pyc
if %pyc_count% gtr 0 (
    echo → Eliminando archivos .pyc...
    for /r %%i in (migrations\*.pyc) do (
        del /q "%%i"
    )
    echo [92m✅ %pyc_count% archivos .pyc eliminados[0m
)

echo.
echo [92m✅ Migraciones eliminadas exitosamente.[0m

:end_migrations
if "%opcion%"=="4" goto recreate_database_no_confirm
echo.
pause
goto inicio

REM ================================================================
REM CONFIRMACIÓN: Recrear base de datos
REM ================================================================
:confirm_database
echo.
echo [91m⚠️  ADVERTENCIA: Esta accion eliminara y recreara la base de datos.[0m
echo [91m   TODOS los datos se perderan de forma permanente.[0m
echo.
set /p confirmacion="[93m¿Desea continuar? (s/n): [0m"
if /i not "%confirmacion%"=="s" (
    echo [93m❌ Operacion cancelada.[0m
    pause
    goto inicio
)

:recreate_database_no_confirm
echo.
echo [95m================================================================[0m
echo [95mTAREA 2: RECREAR BASE DE DATOS MYSQL[0m
echo [95m================================================================[0m
echo.

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo [91m❌ Error: No se encontro el archivo .env[0m
    pause
    goto inicio
)

echo [94m📁 Cargando variables de entorno desde .env...[0m

REM Leer variables del archivo .env
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "line=%%a"
    set "value=%%b"
    
    REM Ignorar líneas en blanco y comentarios
    if not "!line!"=="" (
        echo !line! | findstr /v /r "^#" >nul
        if not errorlevel 1 (
            REM Eliminar comillas simples, dobles y caracteres de nueva línea
            set "value=!value:'=!"
            set "value=!value:"=!"
            
            REM Eliminar espacios y caracteres de control al final
            for /f "tokens=*" %%x in ("!value!") do set "value=%%x"
            
            REM Asignar solo variables de MySQL
            echo %%a | findstr /i "^MYSQL_" >nul
            if not errorlevel 1 (
                set "%%a=!value!"
            )
        )
    )
)

REM Verificar variables necesarias
if "%MYSQL_DB_NAME%"=="" (
    echo [91m❌ Error: Variable MYSQL_DB_NAME no definida en .env[0m
    pause
    goto inicio
)

echo [92m✅ Variables de entorno cargadas correctamente[0m
echo.
echo [94m📊 Configuracion de la base de datos:[0m
echo    → Nombre: [93m%MYSQL_DB_NAME%[0m
echo    → Usuario: [93m%MYSQL_DB_USER%[0m
echo    → Host: [93m%MYSQL_DB_HOST%[0m
echo    → Puerto: [93m%MYSQL_DB_PORT%[0m
echo.

echo [93m🔍 Verificando existencia de la base de datos...[0m

REM Verificar si la base de datos existe
mysql -u"%MYSQL_DB_USER%" -p"%MYSQL_DB_PASSWORD%" -h"%MYSQL_DB_HOST%" -P"%MYSQL_DB_PORT%" -e "SHOW DATABASES LIKE '%MYSQL_DB_NAME%';" 2>nul | findstr /v "Database" > temp_db_check.txt

set DB_EXISTS=0
for /f %%a in (temp_db_check.txt) do set DB_EXISTS=1
del temp_db_check.txt 2>nul

if %DB_EXISTS% equ 1 (
    echo [92m✅ Base de datos '%MYSQL_DB_NAME%' encontrada[0m
    echo.
    
    echo [93m️  Eliminando base de datos existente...[0m
    
    mysql -u"%MYSQL_DB_USER%" -p"%MYSQL_DB_PASSWORD%" -h"%MYSQL_DB_HOST%" -P"%MYSQL_DB_PORT%" -e "DROP DATABASE IF EXISTS `%MYSQL_DB_NAME%`;" 2>nul
    
    if %errorlevel% equ 0 (
        echo [92m✅ Base de datos eliminada exitosamente[0m
    ) else (
        echo [91m❌ Error al eliminar la base de datos[0m
        pause
        goto inicio
    )
) else (
    echo [93m⚠️  La base de datos '%MYSQL_DB_NAME%' no existe[0m
    echo [94mℹ️  Se creara una nueva base de datos[0m
)

echo.
echo [93m🔨 Creando nueva base de datos...[0m

mysql -u"%MYSQL_DB_USER%" -p"%MYSQL_DB_PASSWORD%" -h"%MYSQL_DB_HOST%" -P"%MYSQL_DB_PORT%" -e "CREATE DATABASE `%MYSQL_DB_NAME%` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul

if %errorlevel% equ 0 (
    echo [92m✅ Base de datos creada exitosamente[0m
) else (
    echo [91m❌ Error al crear la base de datos[0m
    pause
    goto inicio
)

echo.
echo [92m✅ Base de datos '%MYSQL_DB_NAME%' recreada exitosamente.[0m

if "%opcion%"=="4" goto delete_virtualenv_no_confirm
echo.
pause
goto inicio

REM ================================================================
REM CONFIRMACIÓN: Eliminar entorno virtual
REM ================================================================
:confirm_virtualenv
echo.
echo [91m⚠️  ADVERTENCIA: Esta accion eliminara el entorno virtual.[0m
echo.
set /p confirmacion="[93m¿Desea continuar? (s/n): [0m"
if /i not "%confirmacion%"=="s" (
    echo [93m❌ Operacion cancelada.[0m
    pause
    goto inicio
)

:delete_virtualenv_no_confirm
echo.
echo [95m================================================================[0m
echo [95mTAREA 3: ELIMINAR ENTORNO VIRTUAL[0m
echo [95m================================================================[0m
echo.

if not exist ".venv" (
    echo [93m⚠️  El entorno virtual no existe (.venv)[0m
    goto end_virtualenv
)

echo [93m🗑️  Eliminando entorno virtual...[0m

rd /s /q .venv

if %errorlevel% equ 0 (
    echo [92m✅ Entorno virtual eliminado exitosamente[0m
) else (
    echo [91m❌ Error al eliminar el entorno virtual[0m
    pause
    goto inicio
)

:end_virtualenv
if "%opcion%"=="4" goto show_instructions
echo.
pause
goto inicio

REM ================================================================
REM CONFIRMACIÓN: Ejecutar todas las tareas
REM ================================================================
:confirm_all
echo.
echo [91m⚠️  ADVERTENCIA: Esta accion realizara las siguientes tareas:[0m
echo [91m   1. Eliminar todas las migraciones[0m
echo [91m   2. Eliminar y recrear la base de datos[0m
echo [91m   3. Eliminar el entorno virtual[0m
echo [91m   TODOS los datos se perderan de forma permanente.[0m
echo.
set /p confirmacion="[93m¿Desea continuar? (s/n): [0m"
if /i not "%confirmacion%"=="s" (
    echo [93m❌ Operacion cancelada.[0m
    pause
    goto inicio
)
goto delete_migrations

REM ================================================================
REM MOSTRAR INSTRUCCIONES FINALES
REM ================================================================
:show_instructions
echo.
echo [96m================================================================[0m
echo [96mINSTRUCCIONES PARA CONTINUAR[0m
echo [96m================================================================[0m
echo.
echo [93m📝 Proximos pasos recomendados:[0m
echo.
echo [94m1. Recrear el entorno virtual:[0m
echo    [93mpython -m venv .venv[0m
echo    [93m.venv\Scripts\activate[0m
echo    [93mpip install -r requirements.txt[0m
echo.
echo [94m2. Crear las migraciones:[0m
echo    [93mpython manage.py makemigrations[0m
echo    [93mpython manage.py migrate[0m
echo.
echo [94m3. Crear el superusuario:[0m
echo    [93mpython create_default_superuser.py[0m
echo.
echo [96m================================================================[0m
echo.
pause
goto inicio

REM ================================================================
REM SALIR
REM ================================================================
:salir
echo.
echo [92m👋 ¡Hasta luego![0m
echo.
exit /b 0
