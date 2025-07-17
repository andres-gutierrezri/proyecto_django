@echo off
echo ================================================================
echo INICIADOR DE APLICACION DJANGO CON ENTORNO VIRTUAL
echo ================================================================

cd /d "%~dp0"

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

echo 🐍 Activando entorno virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Error al activar entorno virtual
    pause
    exit /b 1
)

echo ⬆️  Actualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia: No se pudo actualizar pip, continuando...
)

echo 📦 Instalando dependencias...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas exitosamente
) else (
    echo ⚠️  No se encontró requirements.txt, continuando...
)

echo 🔄 Ejecutando migraciones...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Error al ejecutar migraciones
    pause
    exit /b 1
)

echo ✅ Migraciones completadas

echo 🚀 Iniciando servidor de desarrollo...
echo 📍 URL de la aplicacion: http://127.0.0.1:8000/app_1/
echo ⏹️  Presiona Ctrl+C para detener el servidor

timeout /t 3 /nobreak > nul
start http://127.0.0.1:8000/app_1/

python manage.py runserver 127.0.0.1:8000
