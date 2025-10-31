@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
echo ================================================================
echo INICIADOR DE APLICACIÓN DJANGO CON ENTORNO VIRTUAL
echo ================================================================

cd /d "%~dp0"

REM Verificar que estamos en el directorio correcto
echo 🔍 Verificando estructura del proyecto...
if not exist "manage.py" (
    echo ❌ Error: No se encontró manage.py en el directorio actual
    echo    Asegúrate de que el script esté en la carpeta raíz del proyecto Django
    pause
    exit /b 1
)
echo ✅ Estructura del proyecto verificada

echo 🔍 Detectando y configurando bibliotecas de MySQL...
REM Buscar instalación de MySQL en ubicaciones comunes de Windows
set MYSQL_LIB_PATH=
for %%p in (
    "C:\Program Files\MySQL\MySQL Server 8.0\lib"
    "C:\Program Files\MySQL\MySQL Server 8.4\lib"
    "C:\Program Files (x86)\MySQL\MySQL Server 8.0\lib"
    "C:\MySQL\lib"
    "C:\xampp\mysql\lib"
) do (
    if exist %%p\libmysql.dll (
        set MYSQL_LIB_PATH=%%~p
        goto :mysql_found
    )
)
:mysql_found
if defined MYSQL_LIB_PATH (
    set PATH=%MYSQL_LIB_PATH%;%PATH%
    echo ✅ Bibliotecas de MySQL encontradas en: %MYSQL_LIB_PATH%
    echo    PATH actualizado
) else (
    echo ⚠️  No se encontraron bibliotecas de MySQL en ubicaciones estándar
    echo    Si usas MySQL, asegúrate de tener MySQL instalado correctamente
)

echo 🔍 Verificando entorno virtual...
if not exist ".venv\" (
    echo 🔨 Creando entorno virtual...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Error al crear entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado exitosamente
) else (
    echo ✅ Entorno virtual ya existe
)

echo 🔎 Verificando estado del entorno virtual...
if defined VIRTUAL_ENV (
    echo ✅ Entorno virtual ya está activado: %VIRTUAL_ENV%
) else (
    echo ⚠️  Entorno virtual no está activado, se procederá a activarlo:
    echo 🐍 Activando entorno virtual...
    echo    Ruta de activación: %CD%\.venv\Scripts\activate.bat
    call .venv\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo ❌ Error al activar entorno virtual
        pause
        exit /b 1
        )
    echo ✅ Entorno virtual activado exitosamente
)

echo 📍 Información del entorno virtual:
echo    Ruta: %CD%\.venv
echo    Activación manual: .venv\Scripts\activate.bat
echo    Python: .venv\Scripts\python.exe

echo 🔧 Verificando integridad de pip...
.venv\Scripts\python.exe -c "import pip" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Pip está corrupto, reinstalando entorno virtual...
    echo 🗑️  Eliminando entorno virtual existente...
    rmdir /s /q .venv
    echo 🔨 Creando nuevo entorno virtual...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Error al crear nuevo entorno virtual
        pause
        exit /b 1
    )
    echo 🐍 Activando nuevo entorno virtual...
    call .\.venv\Scripts\activate
    if %errorlevel% neq 0 (
        echo ❌ Error al activar nuevo entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Nuevo entorno virtual creado y activado
    echo 📍 Ruta de activación: %CD%\.venv\Scripts\activate.bat
) else (
    echo ✅ Pip funciona correctamente
    echo ⬆️  Actualizando pip...
    .venv\Scripts\python.exe -m pip install --upgrade pip 2>nul
    if %errorlevel% neq 0 (
        echo 🔧 Intentando reparar pip con ensurepip...
        .venv\Scripts\python.exe -m ensurepip --upgrade 2>nul
        if %errorlevel% neq 0 (
            echo ⚠️  Ensurepip falló, intentando actualización forzada...
            .venv\Scripts\python.exe -m pip install --upgrade --force-reinstall pip 2>nul
            if %errorlevel% neq 0 (
                echo ⚠️  No se pudo actualizar pip, pero continuando con la versión actual...
            ) else (
                echo ✅ Pip actualizado con reinstalación forzada
            )
        ) else (
            echo ✅ Pip reparado con ensurepip
            echo ⬆️  Actualizando pip...
            .venv\Scripts\python.exe -m pip install --upgrade pip 2>nul
        )
    ) else (
        echo ✅ Pip actualizado exitosamente
    )
)

echo 🧹 Limpiando caché de pip...
pip cache purge 2>nul
if %errorlevel% equ 0 (
    echo ✅ Caché de pip limpiado exitosamente
) else (
    echo ⚠️  No se pudo limpiar el caché de pip ^(puede ser normal^)
)

echo 📦 Instalando dependencias...
if exist "requirements.txt" (
    echo 🔍 Verificando pip antes de instalar dependencias...
    .venv\Scripts\python.exe -m pip --version 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  Pip no responde, reinstalando pip...
        .venv\Scripts\python.exe -m ensurepip --upgrade --force 2>nul
        if %errorlevel% neq 0 (
            echo ❌ Error al reinstalar pip
            pause
            exit /b 1
        )
    )
    
    echo 📋 Instalando desde requirements.txt ^(sin caché^)...
    .venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
    if %errorlevel% neq 0 (
        echo ⚠️  Error en instalación, intentando con reinstalación forzada...
        .venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir --force-reinstall
        if %errorlevel% neq 0 (
            echo ❌ Error al instalar dependencias
            echo.
            echo 💡 Sugerencias para solucionar el problema:
            echo    1. Verificar conexión a internet
            echo    2. Ejecutar desde terminal: .venv\Scripts\activate ^&^& pip install --upgrade pip
            echo    3. Instalar dependencias manualmente una por una
            echo.
            echo 🔄 ¿Desea intentar recrear el entorno virtual? ^(s/n^)
            set /p recreate=
            if /i "!recreate!"=="s" (
                echo 🔄 Recreando entorno virtual...
                rmdir /s /q .venv 2>nul
                python -m venv .venv
                if %errorlevel% neq 0 (
                    echo ❌ Error al recrear entorno virtual
                    pause
                    exit /b 1
                )
                call .venv\Scripts\activate
                .venv\Scripts\python.exe -m pip install --upgrade pip
                .venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
                if %errorlevel% neq 0 (
                    echo ❌ Error persistente al instalar dependencias
                    pause
                    exit /b 1
                ) else (
                    echo ✅ Dependencias instaladas después de recrear entorno virtual
                )
            ) else (
                echo ❌ No se pudieron instalar las dependencias
                pause
                exit /b 1
            )
        ) else (
            echo ✅ Dependencias instaladas exitosamente ^(sin caché^)
        )
    ) else (
        echo ✅ Dependencias instaladas exitosamente
    )
) else (
    echo ⚠️  No se encontró requirements.txt, continuando sin instalar dependencias...
)

echo.
echo 📦 Paquetes instalados en el entorno virtual:
echo ================================================================
.venv\Scripts\python.exe -m pip list --format=columns 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  No se pudo obtener la lista de paquetes
) else (
    echo ================================================================
)
echo.

echo 📁 Recolectando archivos estáticos...
.venv\Scripts\python.exe manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia al recolectar archivos estáticos ^(puede ser normal si no está configurado^)
)

echo 🔄 Ejecutando construcción de migraciones...
.venv\Scripts\python.exe manage.py makemigrations
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia al ejecutar makemigrations ^(puede ser normal si no hay cambios^)
)

echo 🔄 Ejecutando migraciones...
.venv\Scripts\python.exe manage.py migrate

if %errorlevel% neq 0 (
    echo ❌ Error al ejecutar migraciones
    pause
    exit /b 1
)

echo ✅ Migraciones completadas

echo 👤 Creando superusuario por defecto ^(si no existe^)...
.venv\Scripts\python.exe create_default_superuser.py
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia al crear superusuario ^(puede ser normal si ya existe^)
)

echo 🔍 Verificando importación de MySQLdb...
.venv\Scripts\python.exe -c "import MySQLdb; print('MySQLdb import successful')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ MySQLdb importado exitosamente
) else (
    echo ⚠️  Advertencia: MySQLdb no pudo ser importado
    echo.
    echo 💡 Soluciones posibles:
    echo    1. Instalar MySQL Server desde: https://dev.mysql.com/downloads/mysql/
    echo.
    echo    2. Agregar MySQL al PATH del sistema
    echo       Ejemplo: C:\Program Files\MySQL\MySQL Server 8.0\lib
    echo.
    echo    3. Reinstalar mysqlclient en el entorno virtual:
    echo       .venv\Scripts\activate
    echo       pip uninstall mysqlclient -y
    echo       pip install mysqlclient --no-cache-dir
    echo.
    echo    4. Si no usas MySQL, puedes cambiar a SQLite en settings.py
    echo.
)

echo 🚀 Iniciando servidor de desarrollo...
echo 📍 URL de la aplicación: http://127.0.0.1:8000/
echo ⏹️  Presiona Ctrl+C para detener el servidor

echo 🌐 Abriendo navegador en segundo plano...
timeout /t 3 /nobreak > nul
start "" http://127.0.0.1:8000/

.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
if %errorlevel% neq 0 (
    echo ❌ Error al iniciar el servidor de desarrollo
    pause
    exit /b 1
)
echo ✅ Servidor de desarrollo detenido
echo ================================================================
echo 👋 Gracias por usar el iniciador de aplicación Django
echo ================================================================
endlocal
