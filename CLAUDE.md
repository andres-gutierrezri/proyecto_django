# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Descripción del Proyecto

Este es un proyecto Django 5.2.3 profesional configurado para la localización en español (Colombia) con soporte multi-base de datos (PostgreSQL, MySQL), despliegue en la nube y almacenamiento en AWS S3. Incluye sistema de plantillas moderno con Bootstrap 5 y DataTables, además de un flujo de configuración automatizado completo.

## Configuración Clave

- **Versión de Django**: 5.2.3
- **Python**: 3.13.0+ requerido
- **Idioma**: Español Colombia (es-co)
- **Zona horaria**: America/Bogota
- **Bases de datos**: PostgreSQL (recomendado), MySQL, SQLite
- **Servidor de producción**: Gunicorn
- **Archivos estáticos**: WhiteNoise con compresión
- **Almacenamiento**: AWS S3 (archivos media), filesystem local (desarrollo)
- **Frontend**: Bootstrap 5.3.0, jQuery 3.6.0, DataTables 1.11.5
- **Entorno virtual**: Directorio `.venv/`
- **Variables de entorno**: python-dotenv (.env file)

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
- `STATIC_URL = '/static/'` (desarrollo) o `'/staticfiles/'` (producción)
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
- WhiteNoise sirve archivos estáticos con compresión y caché optimizado

### Variables de Entorno

El proyecto usa `python-dotenv` para cargar variables desde un archivo `.env`:

```bash
# Crear archivo .env en la raíz del proyecto
# Configuración general
SECRET_KEY=tu-clave-secreta-aqui
IS_DEPLOYED=False  # True en producción
DATABASE_SELECTOR=postgresql  # o mysql
HOSTING_IP_PORT=0.0.0.0:8080
HOSTING_DOMAIN=tu-dominio.com
HOSTING_URL=https://tu-dominio.com

# PostgreSQL (recomendado)
POSTGRESQL_DB_NAME=nombre_bd
POSTGRESQL_DB_USER=usuario
POSTGRESQL_DB_PASSWORD=contraseña
POSTGRESQL_DB_HOST=localhost
POSTGRESQL_DB_PORT=5432
POSTGRESQL_DATABASE_URL=postgres://user:pass@host:port/dbname  # Producción

# MySQL (alternativo)
MYSQL_DB_NAME=nombre_bd
MYSQL_DB_USER=root
MYSQL_DB_PASSWORD=contraseña
MYSQL_DB_HOST=localhost
MYSQL_DB_PORT=3306
MYSQL_DATABASE_URL=mysql://user:pass@host:port/dbname  # Producción

# AWS S3 (opcional)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=tu-bucket
AWS_S3_REGION_NAME=us-east-1
```

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
proyecto/                   # Configuración principal del proyecto
├── settings.py             # Configuración modular de Django
│   ├── Importa: local_settings, cloud_settings, logging_settings
│   ├── DEBUG basado en IS_DEPLOYED
│   ├── Middleware con WhiteNoise
│   └── INSTALLED_APPS incluye whitenoise, storages, humanize
├── local_settings.py       # Configuración de base de datos y entorno
│   ├── IS_DEPLOYED (development/production flag)
│   ├── DATABASE_SELECTOR (postgresql/mysql)
│   └── DATABASE_DICT (configuración dinámica con dj-database-url)
├── cloud_settings.py       # Configuración de AWS S3
│   ├── AWS_ACCESS_KEY_ID
│   ├── AWS_SECRET_ACCESS_KEY
│   ├── AWS_STORAGE_BUCKET_NAME
│   └── AWS_S3_REGION_NAME
├── logging_settings.py     # Sistema de logging
│   └── Logs guardados en tmp/django.log
├── urls.py                 # Configuración de URLs raíz
└── wsgi.py                 # Punto de entrada WSGI

app_1/                      # Aplicación principal de Django
├── models.py               # Modelos de base de datos
├── views.py                # Funciones de vista
├── urls.py                 # Patrones de URL específicos de la aplicación
├── admin.py                # Configuración del panel de administración
├── templates/              # Plantillas HTML
│   ├── base.html           # Plantilla base (Bootstrap 5, DataTables)
│   └── index.html          # Plantilla principal (extiende base.html)
└── static/                 # Recursos estáticos
    ├── css/
    │   └── styles.css      # Estilos personalizados
    ├── js/
    │   ├── script.js                    # Scripts personalizados
    │   ├── initializeDataTables.js      # Inicialización de DataTables
    │   └── themeBasedOnPreference.js    # Tema basado en preferencias
    └── img/
        └── logo.png        # Logo de la aplicación

SQL/                        # Scripts de base de datos
└── MySQL/                  # Scripts SQL para MySQL
    ├── CreateDB.sql        # Crear base de datos
    ├── DeleteTables.sql    # Eliminar tablas
    ├── DropDB.sql          # Eliminar base de datos
    ├── InsertTables.sql    # Insertar datos
    └── QueriesDB.sql       # Consultas de ejemplo

tmp/                        # Archivos temporales
└── django.log              # Logs de Django

Archivos de configuración de despliegue:
├── Procfile                # Configuración para Heroku/Render
├── runtime.txt             # Especifica Python 3.13.0
└── requirements.txt        # Dependencias del proyecto (187 líneas)
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

### Sistema de Plantillas Frontend

El proyecto incluye un sistema de plantillas moderno con herencia:

**Plantilla Base (`app_1/templates/base.html`)**:
- Bootstrap 5.3.0 (CSS framework responsive)
- Google Fonts (Roboto)
- jQuery 3.6.0 (manipulación DOM)
- DataTables 1.11.5 (tablas interactivas con búsqueda, ordenamiento, paginación)
- Popper.js (tooltips y popovers de Bootstrap)
- Bloques personalizables:
  - `{% block titulo %}`: Título de la página
  - `{% block styles %}`: Estilos adicionales
  - `{% block content %}`: Contenido principal
  - `{% block scripts %}`: Scripts adicionales

**JavaScript Personalizado**:
- `initializeDataTables.js`: Función para inicializar DataTables en cualquier tabla
- `themeBasedOnPreference.js`: Detecta y aplica tema claro/oscuro según preferencias del usuario
- `script.js`: Scripts personalizados de la aplicación

**Uso**:
```django
{% extends 'base.html' %}
{% load static %}

{% block titulo %}Mi Página{% endblock %}

{% block styles %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
{% endblock %}

{% block content %}
    <div class="container">
        <!-- Tu contenido aquí -->
    </div>
{% endblock %}

{% block scripts %}
    <script src="{% static 'js/script.js' %}"></script>
{% endblock %}
```

### Scripts SQL para MySQL

El directorio `SQL/MySQL/` contiene scripts útiles para operaciones de base de datos:

- **CreateDB.sql**: Script para crear la base de datos inicial
- **DeleteTables.sql**: Eliminar todas las tablas
- **DropDB.sql**: Eliminar completamente la base de datos
- **InsertTables.sql**: Insertar datos de prueba
- **QueriesDB.sql**: Consultas SQL de ejemplo

Estos scripts son útiles para desarrollo y testing con MySQL.

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

## Despliegue en Producción

El proyecto está completamente preparado para despliegue en plataformas cloud (Heroku, Render, Railway, etc.):

### Configuración de Despliegue

1. **Archivos necesarios**:
   - `Procfile`: Define comando de inicio con Gunicorn (3 workers)
   - `runtime.txt`: Especifica Python 3.13.0
   - WhiteNoise: Configurado para servir archivos estáticos sin nginx

2. **Variables de entorno de producción**:
   ```bash
   IS_DEPLOYED=True
   SECRET_KEY=clave-secreta-segura-generada
   DATABASE_SELECTOR=postgresql  # Recomendado para producción
   POSTGRESQL_DATABASE_URL=postgres://user:pass@host:port/dbname
   HOSTING_DOMAIN=tu-dominio.com
   HOSTING_URL=https://tu-dominio.com
   
   # Opcional: AWS S3 para archivos media
   AWS_ACCESS_KEY_ID=tu-access-key
   AWS_SECRET_ACCESS_KEY=tu-secret-key
   AWS_STORAGE_BUCKET_NAME=tu-bucket
   AWS_S3_REGION_NAME=us-east-1
   ```

3. **Proceso de despliegue** (automático vía Procfile):
   ```bash
   python3 manage.py collectstatic --noinput
   python3 manage.py makemigrations
   python3 manage.py migrate
   gunicorn proyecto.wsgi:application --workers 3 --log-file -
   ```

### Bases de Datos en Producción

- **PostgreSQL** (recomendado):
  - Soportado nativamente por Heroku, Render, Railway
  - Usa `psycopg2-binary` como conector
  - Variable: `POSTGRESQL_DATABASE_URL`

- **MySQL**:
  - Soportado en plataformas que ofrecen MySQL
  - Usa `mysqlclient` como conector
  - Variable: `MYSQL_DATABASE_URL`

- **Selector automático**: El proyecto detecta la variable `DATABASE_SELECTOR` y configura la BD apropiada

### Archivos Estáticos y Media

- **Archivos estáticos**: WhiteNoise sirve desde `staticfiles/` con compresión y caché
- **Archivos media**:
  - Desarrollo: Sistema de archivos local (`media/`)
  - Producción: AWS S3 (si está configurado)

## Notas Importantes

- **Seguridad**: 
  - `SECRET_KEY` debe cargarse desde variables de entorno (.env o plataforma cloud)
  - Nunca commits el archivo `.env` al repositorio (está en .gitignore)
  
- **Modo Debug**: 
  - `DEBUG = not IS_DEPLOYED` (automático según entorno)
  - `DEBUG = False` en producción cuando `IS_DEPLOYED=True`
  
- **Hosts Permitidos**: 
  - Configurado dinámicamente desde variables de entorno
  - Incluye: 127.0.0.1, localhost, HOSTING_IP_PORT, HOSTING_DOMAIN
  
- **Dependencias**: 
  - Total: 187 paquetes en requirements.txt
  - Principales: Django 5.2.3, Gunicorn, WhiteNoise, boto3, psycopg2-binary, mysqlclient
  - Utilidades: python-dotenv, dj-database-url, Pillow, reportlab, XlsxWriter
  
- **Frontend**:
  - Bootstrap 5.3.0 para diseño responsive
  - jQuery 3.6.0 para manipulación DOM
  - DataTables 1.11.5 para tablas interactivas
  - Sistema de plantillas con herencia (base.html)
  
- **Logging**:
  - Logs guardados en `tmp/django.log`
  - Nivel DEBUG para desarrollo
  - Logs de consola en nivel ERROR
  
- **Compatibilidad**: 
  - Al ejecutar comandos de Django en macOS/Linux, usa `python3` en lugar de `python`
  - Scripts de inicio multiplataforma: `.sh` (macOS/Linux), `.bat` (Windows), `.py` (universal)
