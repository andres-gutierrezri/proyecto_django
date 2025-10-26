# Proyecto Django 5.2.3 Profesional

Proyecto Django profesional configurado para desarrollo y producción con soporte multi-base de datos, despliegue en la nube y sistema de plantillas moderno.

## 🚀 Características

- **Django 5.2.3** con Python 3.13.0
- **Multi-base de datos**: PostgreSQL, MySQL con selector dinámico
- **Servidor de producción**: Gunicorn con 3 workers
- **Archivos estáticos**: WhiteNoise con compresión y caché
- **Almacenamiento cloud**: AWS S3 para archivos media (opcional)
- **Frontend moderno**: Bootstrap 5.3.0, jQuery 3.6.0, DataTables 1.11.5
- **Sistema de plantillas**: Herencia de plantillas con base.html
- **Configuración modular**: Settings divididos en local, cloud y logging
- **Variables de entorno**: python-dotenv para configuración segura
- **Scripts de inicio**: Automatización completa del entorno
- **Despliegue cloud**: Compatible con Heroku, Render, Railway
- **Localización**: Español Colombia (es-co), Zona horaria America/Bogota

## 📋 Requisitos

| Software | Versión recomendada |
|----------|--------------------|
| Python   | 3.13.0 o superior |
| PostgreSQL | 12+ (recomendado para producción) |
| MySQL | 8.0+ (alternativo) |
| Git | 2.0+ |
| Dependencias Python | Ver `requirements.txt` (187 paquetes) |

## Configuración inicial para Git

# Eliminar la configuración previa de Git
```bash
# Eliminar la configuración previa de Git
git config --global --unset user.name
git config --global --unset user.email
git config --global --unset credential.helper
git config --global --unset init.defaultBranch
git config --global --unset core.editor
```
# Eliminación completa de las credenciales de Git
```bash
# Eliminar las credenciales almacenadas
git credential-manager uninstall

# Eliminar el perfil de Git
git config --global --remove-section user
git config --global --remove-section credential
git config --global --remove-section init
git config --global --remove-section core

# Eliminar el directorio de configuración de Git
rm -rf ~/.gitconfig

# Eliminar el directorio de credenciales de Git
rm -rf ~/.git-credentials

# Eliminar el directorio de configuración de Git en Windows
rm -rf C:\Users\TuUsuario\.gitconfig

# Eliminar el directorio de credenciales de Git en Windows
rm -rf C:\Users\TuUsuario\.git-credentials

# Listar las configuraciones de Git para verificar que se han eliminado
git config --global --list
```

# Eliminar credenciales específicas de GitHub (alternativa)
```bash
# Eliminar credenciales específicas de GitHub
git credential reject
protocol=https
host=github.com
username=tu_usuario
```

# Eliminación completa de las credenciales y perfil de Git en Windows
```bash
# Listar credenciales almacenadas en Windows
cmdkey /list

# Filtrar credenciales de GitHub
cmdkey /list | findstr github

# Eliminar credenciales específicas de GitHub
cmdkey /delete:git:https://github.com
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

# Configuración de Git
```bash
# Comprobar la versión de Git
git --version

# Configurar el nombre de usuario y correo electrónico
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@example.com"

# Configurar el almacenamiento de credenciales
git config --global credential.helper store

# Configurar la rama principal
git config --global init.defaultBranch main

# Configurar el editor de texto para los mensajes de commit
git config --global core.editor "code --wait" # Para Visual Studio Code

# Comprobar la configuración de Git
git config --list

# Comprobar los remotos de Git
git remote -v
```

## 📁 Estructura del Proyecto

```
proyecto_django/
├── proyecto/                   # Configuración principal
│   ├── settings.py             # Settings modular principal
│   ├── local_settings.py       # Configuración de BD y entorno
│   ├── cloud_settings.py       # Configuración AWS S3
│   ├── logging_settings.py     # Sistema de logging
│   ├── urls.py                 # URLs raíz
│   └── wsgi.py                 # Punto de entrada WSGI
├── app_1/                      # Aplicación principal
│   ├── templates/              # Plantillas HTML
│   │   ├── base.html           # Plantilla base (Bootstrap 5)
│   │   └── index.html          # Página principal
│   ├── static/                 # Archivos estáticos
│   │   ├── css/styles.css
│   │   ├── js/script.js
│   │   ├── js/initializeDataTables.js
│   │   ├── js/themeBasedOnPreference.js
│   │   └── img/logo.png
│   ├── models.py               # Modelos de BD
│   ├── views.py                # Vistas
│   ├── urls.py                 # URLs de la app
│   └── admin.py                # Admin panel
├── SQL/MySQL/                  # Scripts SQL
├── tmp/                        # Archivos temporales
│   └── django.log              # Logs de Django
├── Procfile                    # Config para despliegue cloud
├── runtime.txt                 # Versión de Python (3.13.0)
├── requirements.txt            # Dependencias (187 paquetes)
├── .env                        # Variables de entorno (no commitear)
├── start_server.bat            # Script inicio Windows
├── start_server.sh             # Script inicio macOS/Linux
└── start_server.py             # Script inicio multiplataforma
```

## 🔧 Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# Configuración General
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

# AWS S3 (opcional, para archivos media en producción)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=tu-bucket
AWS_S3_REGION_NAME=us-east-1
```

**⚠️ Importante**: El archivo `.env` está en `.gitignore` y no debe ser commiteado al repositorio.

## 📦 Instalación

### Habilitar la Ejecución de Scripts en PowerShell (Windows)
```powershell
# Directiva de ejecución para el usuario actual
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force

# Comprobar la directiva de ejecución
# Debe mostrar Unrestricted
Get-ExecutionPolicy -List
```

### Verificar la instalación de Python y pip
```bash
# Comprobar la versión de Python
# Windows
python --version
# macOS/Linux
python3 --version

# Verificar la instalación de pip
# Windows
pip --version
# macOS/Linux
pip3 --version

# Actualizar pip
# Windows
python.exe -m pip install --upgrade pip --no-cache-dir
# macOS/Linux
python3 -m pip install --upgrade pip --no-cache-dir

# Actualizar pip a la última versión
pip install --upgrade pip
```

### Instalar entorno virtual de Python
```bash
# Crear entorno virtual
# Windows
python -m venv .venv
# macOS/Linux
python3 -m venv .venv

# Activar el entorno virtual
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Comprobar que el entorno virtual está activado
# Debe mostrar la ruta del entorno virtual
# Windows
python -c "import sys; print(sys.prefix)"
# macOS/Linux
python3 -c "import sys; print(sys.prefix)"

# Actualizar pip dentro del entorno virtual
python -m pip install --upgrade pip --no-cache-dir
```

### Instalar dependencias del proyecto
```bash
# Instalar las 187 dependencias del proyecto
pip install -r requirements.txt --no-cache-dir

# Verificar la instalación de dependencias principales
pip freeze | grep -E "Django|gunicorn|whitenoise|boto3|psycopg2|mysqlclient"

# Comprobar la versión de Django (debe ser 5.2.3)
django-admin --version

# Ver todas las dependencias instaladas
pip list

# Comprobar si hay actualizaciones disponibles
pip list --outdated
```

### Configurar Base de Datos

El proyecto soporta PostgreSQL (recomendado) y MySQL. Configure las variables de entorno en `.env`:

**Para PostgreSQL:**
```bash
DATABASE_SELECTOR=postgresql
POSTGRESQL_DB_NAME=mi_base_datos
POSTGRESQL_DB_USER=mi_usuario
POSTGRESQL_DB_PASSWORD=mi_contraseña
POSTGRESQL_DB_HOST=localhost
POSTGRESQL_DB_PORT=5432
```

**Para MySQL:**
```bash
DATABASE_SELECTOR=mysql
MYSQL_DB_NAME=mi_base_datos
MYSQL_DB_USER=root
MYSQL_DB_PASSWORD=mi_contraseña
MYSQL_DB_HOST=localhost
MYSQL_DB_PORT=3306
```

## 🚀 Uso (Ejecutar el Proyecto)

### Método Automático (Recomendado)

Utilice los scripts de inicio automático que configuran el entorno completo:

```bash
# Windows
start_server.bat

# macOS/Linux
./start_server.sh

# Multiplataforma (Python)
python start_server.py      # Windows
python3 start_server.py     # macOS/Linux
```

**Estos scripts automáticamente:**
1. ✅ Crean/verifican el entorno virtual
2. ✅ Verifican y reparan pip si está corrupto
3. ✅ Instalan/actualizan dependencias desde requirements.txt
4. ✅ Ejecutan makemigrations y migrate
5. ✅ Inician el servidor de desarrollo en http://127.0.0.1:8000/
6. ✅ Abren el navegador automáticamente

### Método Manual

Si prefiere ejecutar los pasos manualmente:

```bash
# Activar entorno virtual
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Crear migraciones (si hay cambios en modelos)
python manage.py makemigrations   # Windows
python3 manage.py makemigrations  # macOS/Linux

# Aplicar migraciones
python manage.py migrate          # Windows
python3 manage.py migrate         # macOS/Linux

# Crear superusuario (opcional, para acceder al admin)
python manage.py createsuperuser  # Windows
python3 manage.py createsuperuser # macOS/Linux

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic    # Windows
python3 manage.py collectstatic   # macOS/Linux

# Iniciar servidor de desarrollo
python manage.py runserver        # Windows
python3 manage.py runserver       # macOS/Linux
```

### Acceder a la Aplicación

- **Página principal**: http://127.0.0.1:8000/app_1/
- **Panel de administración**: http://127.0.0.1:8000/admin/
- **Logs**: Revisa `tmp/django.log` para logs detallados

## 🎨 Frontend y Plantillas

El proyecto incluye un sistema de plantillas moderno:

### Plantilla Base (base.html)
- **Bootstrap 5.3.0**: Framework CSS responsive
- **jQuery 3.6.0**: Manipulación DOM y AJAX
- **DataTables 1.11.5**: Tablas interactivas
- **Google Fonts (Roboto)**: Tipografía moderna

### JavaScript Personalizado
- `initializeDataTables.js`: Inicialización de tablas
- `themeBasedOnPreference.js`: Tema claro/oscuro automático
- `script.js`: Scripts personalizados

### Crear Nuevas Páginas

```django
{% extends 'base.html' %}
{% load static %}

{% block titulo %}Mi Nueva Página{% endblock %}

{% block styles %}
    <link rel="stylesheet" href="{% static 'css/mi-estilo.css' %}">
{% endblock %}

{% block content %}
    <div class="container mt-5">
        <h1>Contenido de mi página</h1>
    </div>
{% endblock %}

{% block scripts %}
    <script src="{% static 'js/mi-script.js' %}"></script>
{% endblock %}
```

## 🚢 Despliegue en Producción

El proyecto está preparado para despliegue en plataformas cloud (Heroku, Render, Railway, etc.):

### Archivos de Configuración

- **Procfile**: Define el comando de inicio con Gunicorn
  ```
  web: python3 manage.py collectstatic && python3 manage.py makemigrations && python3 manage.py migrate && gunicorn proyecto.wsgi:application --workers 3 --log-file -
  ```
- **runtime.txt**: Especifica Python 3.13.0
- **WhiteNoise**: Configurado para servir archivos estáticos sin nginx

### Variables de Entorno para Producción

En la plataforma de despliegue, configure:

```bash
IS_DEPLOYED=True
SECRET_KEY=clave-secreta-segura-generada
DATABASE_SELECTOR=postgresql
POSTGRESQL_DATABASE_URL=postgres://user:pass@host:port/dbname
HOSTING_DOMAIN=tu-dominio.com
HOSTING_URL=https://tu-dominio.com

# Opcional: AWS S3 para archivos media
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=tu-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Plataformas Compatibles

- **Heroku**: PostgreSQL incluido, fácil despliegue con Git
- **Render**: PostgreSQL gratuito, builds automáticos
- **Railway**: PostgreSQL, MySQL disponible
- **DigitalOcean App Platform**: Flexible y escalable
- **AWS Elastic Beanstalk**: Infraestructura AWS completa

### Proceso de Despliegue

1. Conectar repositorio Git a la plataforma
2. Configurar variables de entorno
3. La plataforma ejecutará automáticamente los comandos del Procfile
4. Acceder a la URL proporcionada por la plataforma

## 📚 Bases de Datos

### PostgreSQL (Recomendado para Producción)

```bash
# Instalar PostgreSQL
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb nombre_bd
sudo -u postgres createuser -P nombre_usuario
```

### MySQL (Alternativo)

Scripts SQL disponibles en `SQL/MySQL/`:
- `CreateDB.sql`: Crear base de datos
- `DeleteTables.sql`: Eliminar tablas
- `DropDB.sql`: Eliminar base de datos
- `InsertTables.sql`: Insertar datos de prueba
- `QueriesDB.sql`: Consultas de ejemplo

## 📝 Control de Versiones

### Inicializar Repositorio

```bash
git init
git add .
git commit -m "feat: Proyecto Django inicial"
git branch -M main
git remote add origin https://github.com/USUARIO/proyecto.git
git push -u origin main
```

Para GitLab, sustituya la URL de *origin*.

### Mensajes de Commit Convencionales

Mantenga un historial de commits claro usando el formato convencional:

- **feat**: Nueva característica
  ```bash
  git commit -m "feat: Agregar sistema de autenticación"
  ```

- **fix**: Corrección de errores
  ```bash
  git commit -m "fix: Corregir error en formulario de login"
  ```

- **docs**: Documentación
  ```bash
  git commit -m "docs: Actualizar README con instrucciones de despliegue"
  ```

- **refactor**: Refactorización de código
  ```bash
  git commit -m "refactor: Mejorar estructura de settings"
  ```

- **style**: Cambios de formato
  ```bash
  git commit -m "style: Aplicar formateo PEP8"
  ```

- **test**: Agregar o actualizar tests
  ```bash
  git commit -m "test: Agregar tests para modelo Usuario"
  ```

## 🔒 Seguridad

**Importante:**
- ✅ El archivo `.env` está en `.gitignore` - nunca lo commitee
- ✅ `SECRET_KEY` debe ser único y seguro en producción
- ✅ `DEBUG = False` en producción (controlado por `IS_DEPLOYED=True`)
- ✅ Configure `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` apropiadamente
- ✅ Use HTTPS en producción
- ✅ Mantenga las dependencias actualizadas: `pip list --outdated`

## 📖 Documentación Adicional

- **CLAUDE.md**: Guía detallada para Claude Code con arquitectura y comandos
- **WARP.md**: Guía para WARP con comandos comunes y estructura
- **README.md**: Este archivo con instrucciones generales

## 🤝 Contribuir

1. Fork el proyecto
2. Cree una rama para su característica (`git checkout -b feat/nueva-caracteristica`)
3. Commit sus cambios (`git commit -m 'feat: Agregar nueva característica'`)
4. Push a la rama (`git push origin feat/nueva-caracteristica`)
5. Abra un Pull Request

## 📄 Licencia

© 2025 · Licencia MIT

---

**Desarrollado con ❤️ usando Django 5.2.3**
