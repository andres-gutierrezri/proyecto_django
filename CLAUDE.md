# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Descripción del Proyecto

Este es un proyecto plantilla de inicio para Django 5.2.3 configurado para la localización en español (Colombia) con base de datos SQLite. Sirve como ejemplo fundamental para construir aplicaciones web Django con un flujo de configuración automatizado completo.

## Configuración Clave

- **Versión de Django**: 5.2.3
- **Python**: 3.10+ requerido
- **Idioma**: Español Colombia (es-co)
- **Zona horaria**: America/Bogota
- **Base de datos**: SQLite (db.sqlite3)
- **Entorno virtual**: Directorio `.venv/`

## Comandos de Desarrollo

### Iniciar el Servidor

**Inicio automático (recomendado):**
```bash
# macOS/Linux
./start_server.sh

# Windows
start_server.bat

# Script Python multiplataforma
python3 start_server.py    # macOS/Linux
python start_server.py     # Windows
```

Estos scripts automáticamente:
1. Crean/verifican el entorno virtual
2. Verifican y reparan pip si está corrupto
3. Instalan/actualizan dependencias desde requirements.txt
4. Ejecutan makemigrations y migrate
5. Inician el servidor de desarrollo en http://127.0.0.1:8000/
6. Abren el navegador automáticamente

**Inicio manual:**
```bash
# Activar entorno virtual
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py makemigrations  # Windows
python3 manage.py makemigrations # macOS/Linux

python manage.py migrate         # Windows
python3 manage.py migrate        # macOS/Linux

# Iniciar servidor
python manage.py runserver 127.0.0.1:8000   # Windows
python3 manage.py runserver 127.0.0.1:8000  # macOS/Linux
```

### Operaciones de Base de Datos

```bash
# Crear migraciones para cambios en modelos
python manage.py makemigrations   # Windows
python3 manage.py makemigrations  # macOS/Linux

# Aplicar migraciones
python manage.py migrate          # Windows
python3 manage.py migrate         # macOS/Linux

# Crear superusuario para el panel de administración
python manage.py createsuperuser  # Windows
python3 manage.py createsuperuser # macOS/Linux

# Abrir shell de Django
python manage.py shell            # Windows
python3 manage.py shell           # macOS/Linux
```

### Archivos Estáticos

```bash
# Recolectar archivos estáticos a STATIC_ROOT
python manage.py collectstatic    # Windows
python3 manage.py collectstatic   # macOS/Linux
```

Los archivos estáticos están configurados con:
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `STATICFILES_DIRS = [BASE_DIR / 'app_1/static']`

## Arquitectura del Proyecto

### Estructura de Enrutamiento de URLs

El proyecto utiliza una configuración de URLs de dos niveles:

1. **Nivel de proyecto** (`proyecto/urls.py`):
   - URL raíz (`''`) incluye todas las rutas de `app_1.urls`
   - Panel de administración en `/admin/`

2. **Nivel de aplicación** (`app_1/urls.py`):
   - Vista principal de la app en `/app_1/`

Esto significa que la aplicación es accesible tanto desde el dominio raíz como desde la ruta `/app_1/`.

### Estructura de la Aplicación

```
proyecto/               # Configuración principal del proyecto
├── settings.py         # Configuración de Django (SECRET_KEY, DATABASES, INSTALLED_APPS)
├── urls.py            # Configuración de URLs raíz
└── wsgi.py            # Punto de entrada de la aplicación WSGI

app_1/                 # Aplicación principal de Django
├── models.py          # Modelos de base de datos (actualmente vacío)
├── views.py           # Funciones de vista (renderiza la plantilla index.html)
├── urls.py            # Patrones de URL específicos de la aplicación
├── admin.py           # Configuración del panel de administración
├── templates/         # Plantillas HTML
│   └── index.html     # Plantilla principal
└── static/            # Recursos estáticos
    ├── css/
    ├── js/
    └── img/
```

### Gestión del Entorno Virtual

Los scripts de inicio (`start_server.py`, `start_server.bat`, `start_server.sh`) incluyen manejo sofisticado del entorno virtual:

- **Verificaciones de integridad**: Verifican la funcionalidad de pip antes de continuar
- **Auto-reparación**: Si pip está corrupto, recrea automáticamente el entorno virtual
- **Estrategias de respaldo**: Múltiples métodos de instalación/actualización de pip (ensurepip, force-reinstall, get-pip.py)
- **Instalación de dependencias**: Intenta instalación normal primero, luego con `--no-cache-dir` si falla
- **Recuperación interactiva**: Solicita al usuario recrear el entorno si falla la instalación de dependencias

**Diferencias entre plataformas:**
- **Windows**: Usa `python`, `.venv\Scripts\`, `start ""` para abrir navegador
- **macOS/Linux**: Usa `python3`, `.venv/bin/`, `open` para abrir navegador (macOS) o `xdg-open` (Linux)

Al modificar estos scripts, mantén los mismos patrones de manejo de errores y retroalimentación al usuario (mensajes de estado basados en emojis).

## Flujo de Trabajo con Git

Este proyecto sigue el formato de mensajes de commit convencionales. Usa prefijos:
- `feat:` para nuevas características
- `fix:` para correcciones de errores
- `docs:` para documentación
- `refactor:` para refactorización de código

Ejemplo de commits recientes:
```
feat: Mejorar verificación y manejo de errores en el script de inicio de Django
```

## Agregar Nuevas Aplicaciones

Al crear nuevas aplicaciones Django:

1. Crear la aplicación:
   ```bash
   python manage.py startapp app_name   # Windows
   python3 manage.py startapp app_name  # macOS/Linux
   ```
2. Agregar a `INSTALLED_APPS` en `proyecto/settings.py`
3. Crear patrones de URL en `app_name/urls.py`
4. Incluir URLs de la aplicación en `proyecto/urls.py` usando `include()`
5. Agregar archivos estáticos a `STATICFILES_DIRS` si es necesario

## Notas Importantes

- **Seguridad**: La `SECRET_KEY` actual en settings.py es solo para desarrollo. Reemplázala en producción.
- **Modo Debug**: `DEBUG = True` está configurado para desarrollo. Cambia a `False` en producción.
- **Hosts Permitidos**: Actualmente limitado a `['127.0.0.1', 'localhost']`. Actualiza para despliegue en producción.
- **Dependencias**: El proyecto incluye `mysql-connector-python` en requirements.txt para soporte opcional de MySQL, aunque actualmente está configurado SQLite.
- **Compatibilidad**: Al ejecutar comandos de Django en macOS/Linux, usa `python3` en lugar de `python`.
