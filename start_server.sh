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

echo "🔍 Detectando y configurando bibliotecas de MySQL..."
# Buscar instalación de MySQL en ubicaciones comunes de macOS
MYSQL_BASE_PATHS=(
    "/usr/local/mysql"
    "/opt/homebrew/opt/mysql"
    "/usr/local/opt/mysql"
    "/opt/homebrew/Cellar/mysql/"*
    "/usr/local/Cellar/mysql/"*
)

MYSQL_ROOT=""
for path_pattern in "${MYSQL_BASE_PATHS[@]}"; do
    # Expandir patrones con comodines
    for path in $path_pattern; do
        if [ -d "$path/lib" ] && [ -f "$path/lib/libmysqlclient.dylib" -o -f "$path/lib/libmysqlclient.24.dylib" ]; then
            MYSQL_ROOT="$path"
            break 2
        fi
    done
done

if [ -n "$MYSQL_ROOT" ]; then
    # Configurar todas las variables de entorno necesarias para MySQL
    export PATH="$MYSQL_ROOT/bin:$PATH"
    export MYSQLCLIENT_CFLAGS="-I$MYSQL_ROOT/include"
    export MYSQLCLIENT_LDFLAGS="-L$MYSQL_ROOT/lib -lmysqlclient"
    export PKG_CONFIG_PATH="$MYSQL_ROOT/lib/pkgconfig"
    export DYLD_LIBRARY_PATH="$MYSQL_ROOT/lib:$DYLD_LIBRARY_PATH"
    export DYLD_FALLBACK_LIBRARY_PATH="$MYSQL_ROOT/lib:$DYLD_FALLBACK_LIBRARY_PATH"
    
    echo "✅ MySQL encontrado en: $MYSQL_ROOT"
    echo "   Variables de entorno configuradas:"
    echo "   - PATH"
    echo "   - MYSQLCLIENT_CFLAGS"
    echo "   - MYSQLCLIENT_LDFLAGS"
    echo "   - PKG_CONFIG_PATH"
    echo "   - DYLD_LIBRARY_PATH"
    echo "   - DYLD_FALLBACK_LIBRARY_PATH"
else
    echo "⚠️  No se encontraron bibliotecas de MySQL en ubicaciones estándar"
    echo "   Si usas MySQL, asegúrate de tener MySQL instalado correctamente"
    echo "   Puedes instalar MySQL con: brew install mysql"
    echo ""
    echo "   O agregar estas variables a tu ~/.zprofile:"
    echo "   export PATH=\"/usr/local/mysql/bin:\$PATH\""
    echo "   export MYSQLCLIENT_CFLAGS=\"-I/usr/local/mysql/include\""
    echo "   export MYSQLCLIENT_LDFLAGS=\"-L/usr/local/mysql/lib -lmysqlclient\""
    echo "   export PKG_CONFIG_PATH=\"/usr/local/mysql/lib/pkgconfig\""
    echo "   export DYLD_LIBRARY_PATH=\"/usr/local/mysql/lib:\$DYLD_LIBRARY_PATH\""
    echo "   export DYLD_FALLBACK_LIBRARY_PATH=\"/usr/local/mysql/lib:\$DYLD_FALLBACK_LIBRARY_PATH\""
fi

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
    VENV_ACTIVATE_PATH="$(pwd)/.venv/bin/activate"
    echo "   Ruta de activación: $VENV_ACTIVATE_PATH"
    source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Error al activar entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual activado exitosamente"
fi

echo "📍 Información del entorno virtual:"
echo "   Ruta: $(pwd)/.venv"
echo "   Activación manual: source .venv/bin/activate"
echo "   Python: .venv/bin/python"

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
    echo "📍 Ruta de activación: $(pwd)/.venv/bin/activate"
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

echo "🧹 Limpiando caché de pip..."
pip3 cache purge 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Caché de pip limpiado exitosamente"
else
    echo "⚠️  No se pudo limpiar el caché de pip (puede ser normal)"
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

    echo "📋 Instalando desde requirements.txt (sin caché)..."
    .venv/bin/python -m pip install -r requirements.txt --no-cache-dir
    if [ $? -ne 0 ]; then
        echo "⚠️  Error en instalación, intentando con reinstalación forzada..."
        .venv/bin/python -m pip install -r requirements.txt --no-cache-dir --force-reinstall
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

echo ""
echo "📦 Paquetes instalados en el entorno virtual:"
echo "================================================================"
.venv/bin/python -m pip list --format=columns 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  No se pudo obtener la lista de paquetes"
else
    echo "================================================================"
fi
echo ""

echo "📁 Recolectando archivos estáticos..."
.venv/bin/python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia al recolectar archivos estáticos (puede ser normal si no está configurado)"
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

echo "👤 Creando superusuario por defecto (si no existe)..."
.venv/bin/python create_default_superuser.py
if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia al crear superusuario (puede ser normal si ya existe)"
fi

echo "🔍 Verificando importación de MySQLdb..."
.venv/bin/python -c "import MySQLdb; print('MySQLdb import successful')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ MySQLdb importado exitosamente"
else
    echo "⚠️  Advertencia: MySQLdb no pudo ser importado"
    echo ""
    echo "💡 Soluciones posibles:"
    echo "   1. Instalar MySQL:"
    echo "      brew install mysql"
    echo ""
    echo "   2. Agregar variables de entorno de MySQL a ~/.zprofile:"
    echo "      export PATH=\"/usr/local/mysql/bin:\$PATH\""
    echo "      export MYSQLCLIENT_CFLAGS=\"-I/usr/local/mysql/include\""
    echo "      export MYSQLCLIENT_LDFLAGS=\"-L/usr/local/mysql/lib -lmysqlclient\""
    echo "      export PKG_CONFIG_PATH=\"/usr/local/mysql/lib/pkgconfig\""
    echo "      export DYLD_LIBRARY_PATH=\"/usr/local/mysql/lib:\$DYLD_LIBRARY_PATH\""
    echo "      export DYLD_FALLBACK_LIBRARY_PATH=\"/usr/local/mysql/lib:\$DYLD_FALLBACK_LIBRARY_PATH\""
    echo ""
    echo "   3. Reinstalar mysqlclient con las variables configuradas:"
    echo "      source .venv/bin/activate"
    echo "      pip uninstall mysqlclient -y"
    echo "      pip install mysqlclient --no-cache-dir"
    echo ""
    echo "   4. Si no usas MySQL, puedes cambiar a SQLite en settings.py"
    echo ""
    
    # Intentar detectar si MySQL está instalado
    if command -v mysql >/dev/null 2>&1; then
        MYSQL_CONFIG=$(which mysql_config 2>/dev/null)
        if [ -n "$MYSQL_CONFIG" ]; then
            MYSQL_LIB=$($MYSQL_CONFIG --libs 2>/dev/null | grep -o '\-L[^ ]*' | sed 's/-L//')
            if [ -n "$MYSQL_LIB" ]; then
                MYSQL_BASE=$(dirname "$MYSQL_LIB")
                echo "   📌 MySQL detectado en: $MYSQL_BASE"
                echo "   Asegúrate de tener estas variables en tu ~/.zprofile"
            fi
        fi
    else
        echo "   ⚠️  MySQL no parece estar instalado en el sistema"
    fi
    echo ""
fi

echo "🚀 Iniciando servidor de desarrollo..."
echo "📍 URL de la aplicación: http://127.0.0.1:8000/"
echo "⏹️  Presiona Ctrl+C para detener el servidor"

echo "🌐 Abriendo navegador en segundo plano..."
sleep 3
open http://127.0.0.1:8000/

.venv/bin/python manage.py runserver 127.0.0.1:8000
if [ $? -ne 0 ]; then
    echo "❌ Error al iniciar el servidor de desarrollo"
    exit 1
fi
echo "✅ Servidor de desarrollo detenido"
echo "================================================================"
echo "👋 Gracias por usar el iniciador de aplicación Django"
echo "================================================================"
