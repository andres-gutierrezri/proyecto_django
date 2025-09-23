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
    call .venv\Scripts\activate.bat
    if %errorlevel% neq 0 (
        echo ❌ Error al activar entorno virtual
        pause
        exit /b 1
        )
)

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
    
    echo 📋 Instalando desde requirements.txt...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ⚠️  Error en instalación normal, intentando con --no-cache-dir...
        .venv\Scripts\python.exe -m pip install -r requirements.txt --no-cache-dir
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

echo 🚀 Iniciando servidor de desarrollo...
echo 📍 URL de la aplicación: http://127.0.0.1:8000/
echo ⏹️  Presiona Ctrl+C para detener el servidor

echo 🌐 Abriendo navegador en segundo plano...
timeout /t 3 /nobreak > nul
start "" http://127.0.0.1:8000/

.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000