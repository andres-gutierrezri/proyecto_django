#!/bin/bash

echo "================================================================"
echo "INICIADOR DE APLICACIÓN DJANGO CON ENTORNO VIRTUAL"
echo "================================================================"

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar que estamos en el directorio correcto
echo "🔍 Verificando estructura del proyecto..."
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encontró manage.py en el directorio actual"
    echo "   Asegúrate de que el script esté en la carpeta raíz del proyecto Django"
    exit 1
fi
echo "✅ Estructura del proyecto verificada"

echo "🔍 Verificando entorno virtual..."
if [ ! -d ".venv" ]; then
    echo "🔨 Creando entorno virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado exitosamente"
else
    echo "✅ Entorno virtual ya existe"
fi

echo "🔎 Verificando estado del entorno virtual..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Entorno virtual ya está activado: $VIRTUAL_ENV"
else
    echo "⚠️  Entorno virtual no está activado, se procederá a activarlo:"
    echo "🐍 Activando entorno virtual..."
    source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Error al activar entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual activado exitosamente"
fi

echo "🔧 Verificando integridad de pip..."
.venv/bin/python -c "import pip" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Pip está corrupto, reinstalando entorno virtual..."
    echo "🗑️  Eliminando entorno virtual existente..."
    rm -rf .venv
    echo "🔨 Creando nuevo entorno virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear nuevo entorno virtual"
        exit 1
    fi
    echo "🐍 Activando nuevo entorno virtual..."
    source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Error al activar nuevo entorno virtual"
        exit 1
    fi
    echo "✅ Nuevo entorno virtual creado y activado"
else
    echo "✅ Pip funciona correctamente"
    echo "⬆️  Actualizando pip..."
    .venv/bin/python -m pip install --upgrade pip 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "🔧 Intentando reparar pip con ensurepip..."
        .venv/bin/python -m ensurepip --upgrade 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "⚠️  Ensurepip falló, intentando actualización forzada..."
            .venv/bin/python -m pip install --upgrade --force-reinstall pip 2>/dev/null
            if [ $? -ne 0 ]; then
                echo "⚠️  No se pudo actualizar pip, pero continuando con la versión actual..."
            else
                echo "✅ Pip actualizado con reinstalación forzada"
            fi
        else
            echo "✅ Pip reparado con ensurepip"
            echo "⬆️  Actualizando pip..."
            .venv/bin/python -m pip install --upgrade pip 2>/dev/null
        fi
    else
        echo "✅ Pip actualizado exitosamente"
    fi
fi

echo "📦 Instalando dependencias..."
if [ -f "requirements.txt" ]; then
    echo "🔍 Verificando pip antes de instalar dependencias..."
    .venv/bin/python -m pip --version 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  Pip no responde, reinstalando pip..."
        .venv/bin/python -m ensurepip --upgrade --force 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌ Error al reinstalar pip"
            exit 1
        fi
    fi

    echo "📋 Instalando desde requirements.txt..."
    .venv/bin/python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "⚠️  Error en instalación normal, intentando con --no-cache-dir..."
        .venv/bin/python -m pip install -r requirements.txt --no-cache-dir
        if [ $? -ne 0 ]; then
            echo "❌ Error al instalar dependencias"
            echo ""
            echo "💡 Sugerencias para solucionar el problema:"
            echo "   1. Verificar conexión a internet"
            echo "   2. Ejecutar desde terminal: source .venv/bin/activate && pip install --upgrade pip"
            echo "   3. Instalar dependencias manualmente una por una"
            echo ""
            read -p "🔄 ¿Desea intentar recrear el entorno virtual? (s/n): " recreate
            if [ "$recreate" = "s" ] || [ "$recreate" = "S" ]; then
                echo "🔄 Recreando entorno virtual..."
                rm -rf .venv 2>/dev/null
                python3 -m venv .venv
                if [ $? -ne 0 ]; then
                    echo "❌ Error al recrear entorno virtual"
                    exit 1
                fi
                source .venv/bin/activate
                .venv/bin/python -m pip install --upgrade pip
                .venv/bin/python -m pip install -r requirements.txt --no-cache-dir
                if [ $? -ne 0 ]; then
                    echo "❌ Error persistente al instalar dependencias"
                    exit 1
                else
                    echo "✅ Dependencias instaladas después de recrear entorno virtual"
                fi
            else
                echo "❌ No se pudieron instalar las dependencias"
                exit 1
            fi
        else
            echo "✅ Dependencias instaladas exitosamente (sin caché)"
        fi
    else
        echo "✅ Dependencias instaladas exitosamente"
    fi
else
    echo "⚠️  No se encontró requirements.txt, continuando sin instalar dependencias..."
fi

echo "🔄 Ejecutando construcción de migraciones..."
.venv/bin/python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia al ejecutar makemigrations (puede ser normal si no hay cambios)"
fi

echo "🔄 Ejecutando migraciones..."
.venv/bin/python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Error al ejecutar migraciones"
    exit 1
fi

echo "✅ Migraciones completadas"

echo "🚀 Iniciando servidor de desarrollo..."
echo "📍 URL de la aplicación: http://127.0.0.1:8000/"
echo "⏹️  Presiona Ctrl+C para detener el servidor"

echo "🌐 Abriendo navegador en segundo plano..."
sleep 3
open http://127.0.0.1:8000/

.venv/bin/python manage.py runserver 127.0.0.1:8000
