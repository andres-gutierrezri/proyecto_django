# Proyecto Django 5.2.3 Profesional

Proyecto Django profesional configurado para desarrollo y producción con soporte multi-base de datos, despliegue en la nube y sistema de plantillas moderno.

## 🚀 Características

- **Django 5.2.3** con Python 3.13.0
- **Sistema de autenticación completo**: Registro, login, verificación de email, protección de vistas
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
- **Seguridad**: Contraseñas cifradas, protección CSRF, validación compleja de contraseñas

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
│   ├── wsgi.py                 # Punto de entrada WSGI
│   ├── static/                 # Archivos estáticos del proyecto
│   └── templates/              # Plantillas del proyecto
│       └── common/
│           └── auth_base.html  # Base para autenticación
├── app_1/                      # Aplicación principal
│   ├── models.py               # CustomUser y otros modelos
│   ├── forms.py                # Formularios de autenticación
│   ├── validators.py           # Validadores personalizados
│   ├── views.py                # Vistas de autenticación
│   ├── utils.py                # Utilidades de email
│   ├── urls.py                 # URLs de la aplicación
│   ├── admin.py                # Admin personalizado
│   ├── templates/app_1/        # Plantillas de la app
│   │   ├── page_login.html     # Página de login
│   │   ├── page_register.html  # Página de registro
│   │   ├── dashboard.html      # Dashboard de usuario
│   │   └── emails/             # Templates de email
│   │       ├── verification_email.html
│   │       └── login_notification.html
│   ├── static/app_1/           # Archivos estáticos
│   │   ├── css/
│   │   │   ├── page_login.css
│   │   │   └── page_register.css
│   │   ├── js/
│   │   │   ├── page_login.js
│   │   │   ├── page_register.js
│   │   │   ├── initializeDataTables.js
│   │   │   └── themeBasedOnPreference.js
│   │   └── img/
│   │       └── logo.png
│   └── migrations/             # Migraciones de BD
│       └── 0001_initial.py     # Migración inicial CustomUser
├── SQL/MySQL/                  # Scripts SQL
│   ├── CreateDB.sql
│   ├── DeleteTables.sql
│   ├── DropDB.sql
│   ├── InsertTables.sql
│   └── QueriesDB.sql
├── tmp/                        # Archivos temporales
│   └── django.log              # Logs de Django
├── .env                        # Variables de entorno (no commitear)
├── .gitignore                  # Archivos ignorados por Git
├── Procfile                    # Config Heroku/Render
├── nixpacks.toml               # Config Railway/Nixpacks
├── runtime.txt                 # Versión Python (3.13.0)
├── requirements.txt            # Dependencias (187 paquetes)
├── manage.py                   # Script de gestión Django
├── start_server.bat            # Script inicio Windows
├── start_server.sh             # Script inicio macOS/Linux
├── start_server.py             # Script inicio multiplataforma
├── README.md                   # Documentación principal
├── CLAUDE.md                   # Guía para Claude Code
└── WARP.md                     # Guía para WARP
```

## 🔧 Configuración de Variables de Entorno

El proyecto incluye un archivo [.env](.env) de ejemplo con todas las variables necesarias completamente documentadas. Configura las siguientes variables según tu entorno:

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

# Configuración de Email (Sistema de Autenticación)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Desarrollo
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  # Producción
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación-de-google
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

**⚠️ Importante**:
- El archivo `.env` está en `.gitignore` y NO debe ser commiteado al repositorio
- El proyecto ya incluye un archivo `.env` de ejemplo con todas las variables documentadas
- Para Gmail, genera una "Contraseña de aplicación" en https://myaccount.google.com/apppasswords
- Consulta el archivo [.env](.env) para ver la documentación completa de cada variable

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

- **Página de login**: http://127.0.0.1:8000/ o http://127.0.0.1:8000/login/
- **Página de registro**: http://127.0.0.1:8000/register/
- **Dashboard (requiere login)**: http://127.0.0.1:8000/dashboard/
- **Panel de administración**: http://127.0.0.1:8000/admin/
- **Logs**: Revisa `tmp/django.log` para logs detallados

## 🔐 Sistema de Autenticación

El proyecto incluye un sistema completo de autenticación de usuarios listo para usar.

### Características del Sistema de Autenticación

1. **Registro de Usuarios**
   - ✅ Email como nombre de usuario único
   - ✅ Validación compleja de contraseñas (8-20 caracteres, mayúsculas, minúsculas, caracteres especiales)
   - ✅ Verificación de términos y condiciones
   - ✅ Opción de suscripción a newsletter
   - ✅ Envío automático de email de verificación

2. **Inicio de Sesión**
   - ✅ Autenticación con email y contraseña
   - ✅ Opción "Recordarme" (sesión de 30 días)
   - ✅ Notificación por email al iniciar sesión
   - ✅ Mensajes contextuales (usuario no registrado, contraseña incorrecta, cuenta inactiva)

3. **Seguridad**
   - ✅ Contraseñas cifradas con sistema de Django
   - ✅ Protección CSRF en todos los formularios
   - ✅ Validación de contraseñas: mínimo 8 caracteres, letra mayúscula, minúscula, carácter especial
   - ✅ Sin espacios ni emojis en contraseñas
   - ✅ Tokens seguros para verificación de email

4. **Protección de Vistas**
   - ✅ Decorador `@login_required` para vistas protegidas
   - ✅ Redirección automática al login si no autenticado
   - ✅ Dashboard accesible solo para usuarios autenticados

### Estructura de Archivos de Autenticación

```
app_1/
├── models.py                   # CustomUser (extiende AbstractUser)
├── forms.py                    # Formularios de registro y login
├── validators.py               # PasswordComplexityValidator
├── views.py                    # Vistas de autenticación
├── utils.py                    # Utilidades de email
├── admin.py                    # Admin personalizado para CustomUser
├── templates/app_1/
│   ├── page_login.html         # Formulario de login
│   ├── page_register.html      # Formulario de registro
│   ├── dashboard.html          # Panel de usuario
│   └── emails/
│       ├── verification_email.html     # Email de verificación
│       └── login_notification.html     # Email de notificación
└── urls.py                     # URLs de autenticación
```

### Modelo CustomUser

El proyecto usa un modelo de usuario personalizado ([app_1/models.py](app_1/models.py)) con campos adicionales:

- `email` - Correo electrónico único (usado como username)
- `first_name` - Nombre (obligatorio)
- `last_name` - Apellido (obligatorio)
- `email_verified` - Estado de verificación de email
- `email_verification_token` - Token de verificación
- `notify_on_login` - Preferencia de notificaciones
- `terms_accepted` - Aceptación de términos
- `newsletter_subscription` - Suscripción al boletín

### Configuración de Email

Por defecto, los emails se muestran en la consola del servidor (modo desarrollo). Para enviar emails reales en producción:

**Agregar al archivo `.env`:**

```bash
# Configuración de Email para Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación-de-google
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

**Importante**:
- Para Gmail, genera una "Contraseña de aplicación" en https://myaccount.google.com/apppasswords
- NO uses tu contraseña normal de Gmail
- Activa la verificación en dos pasos primero

### Uso del Sistema de Autenticación

#### 1. Registrar un Nuevo Usuario

```bash
# 1. Navegar a la página de registro
http://127.0.0.1:8000/register/

# 2. Completar el formulario:
#    - Nombre y apellido
#    - Email válido (será tu username)
#    - Contraseña (mínimo 8 caracteres, mayúscula, minúscula, carácter especial)
#    - Aceptar términos y condiciones

# 3. El sistema enviará un email de verificación
#    En desarrollo: Revisar la consola del servidor
#    En producción: Revisar el correo electrónico

# 4. Hacer clic en el enlace de verificación
```

#### 2. Iniciar Sesión

```bash
# 1. Navegar a la página de login
http://127.0.0.1:8000/login/

# 2. Ingresar:
#    - Email registrado
#    - Contraseña

# 3. Opcional: Marcar "Recordarme" para sesión de 30 días

# 4. Tras iniciar sesión:
#    - Redirección al dashboard
#    - Email de notificación (si está configurado)
```

#### 3. Acceder al Dashboard

Una vez autenticado, accede a tu panel de usuario:

```bash
http://127.0.0.1:8000/dashboard/
```

Aquí verás:
- Información de tu cuenta
- Estado de verificación de email
- Preferencias de newsletter
- Opción para cerrar sesión

#### 4. Panel de Administración

Para gestionar usuarios desde el admin de Django:

```bash
# 1. Crear un superusuario
source .venv/bin/activate
python3 manage.py createsuperuser  # macOS/Linux
python manage.py createsuperuser   # Windows

# 2. Acceder al panel de administración
http://127.0.0.1:8000/admin/

# 3. Gestionar usuarios, permisos y más
```

### Validación de Contraseñas

El sistema valida contraseñas con requisitos estrictos ([app_1/validators.py](app_1/validators.py)):

```python
✅ Mínimo 8 caracteres
✅ Máximo 20 caracteres
✅ Al menos una letra mayúscula (A-Z)
✅ Al menos una letra minúscula (a-z)
✅ Al menos un carácter especial (!@#$%^&*()_+-=[]{}|;:,.<>?)
❌ Sin espacios
❌ Sin emojis
```

**Ejemplos:**
- ✅ `MiPass123!` - Válida
- ✅ `Secure@2025` - Válida
- ❌ `password` - Sin mayúscula ni carácter especial
- ❌ `PASSWORD123` - Sin minúscula ni carácter especial
- ❌ `Pass 123!` - Contiene espacio

### Mensajes de Error y Validación

#### En Registro:
- **Email duplicado**: "Ya existe un usuario con este correo electrónico"
- **Contraseña débil**: Mensajes específicos del validador que falle
- **Términos no aceptados**: "Debes aceptar antes de continuar"

#### En Login:
- **Email no registrado**: "No existe una cuenta con este correo electrónico. ¿Deseas registrarte?"
- **Contraseña incorrecta**: "Contraseña incorrecta"
- **Cuenta inactiva**: "Tu cuenta está inactiva. Por favor contacta al soporte"

### Proteger Vistas Personalizadas

Para proteger tus propias vistas y requerir autenticación:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def mi_vista_protegida(request):
    """
    Solo usuarios autenticados pueden acceder.
    Redirige al login si no están autenticados.
    """
    context = {
        'usuario': request.user,
    }
    return render(request, 'mi_template.html', context)
```

### URLs de Autenticación

Las siguientes rutas están disponibles ([app_1/urls.py](app_1/urls.py)):

| URL | Nombre | Descripción |
|-----|--------|-------------|
| `/` | `page_login` | Página de inicio de sesión |
| `/login/` | `login` | Página de inicio de sesión (alternativa) |
| `/register/` | `page_register` | Página de registro |
| `/logout/` | `logout` | Cerrar sesión |
| `/verify-email/<token>/` | `verify_email` | Verificar email con token |
| `/dashboard/` | `dashboard` | Panel de usuario (protegido) |

### Emails del Sistema

El sistema envía dos tipos de emails automáticamente:

#### 1. Email de Verificación
- **Cuándo**: Al registrarse un nuevo usuario
- **Contenido**: Enlace de verificación con token único
- **Plantilla**: [app_1/templates/app_1/emails/verification_email.html](app_1/templates/app_1/emails/verification_email.html)
- **Diseño**: HTML con gradiente morado, responsive

#### 2. Email de Notificación de Login
- **Cuándo**: Al iniciar sesión (si está activado en preferencias)
- **Contenido**: Fecha, hora, IP, dispositivo
- **Plantilla**: [app_1/templates/app_1/emails/login_notification.html](app_1/templates/app_1/emails/login_notification.html)
- **Propósito**: Seguridad y notificación de actividad

### Personalización

Puedes personalizar el sistema de autenticación:

**Cambiar los templates:**
```bash
app_1/templates/app_1/
├── page_login.html      # Diseño del formulario de login
├── page_register.html   # Diseño del formulario de registro
└── dashboard.html       # Diseño del panel de usuario
```

**Modificar validadores:**
```python
# app_1/validators.py
class PasswordComplexityValidator:
    def validate(self, password, user=None):
        # Personaliza las reglas de validación
        pass
```

**Cambiar emails:**
```bash
app_1/templates/app_1/emails/
├── verification_email.html     # Email de verificación
└── login_notification.html     # Email de notificación
```

### Consideraciones de Seguridad

1. **Contraseñas**: Se cifran automáticamente con el sistema de Django (PBKDF2)
2. **Tokens**: Generados con `secrets.token_urlsafe(32)` - criptográficamente seguros
3. **CSRF**: Protección activa en todos los formularios con `{% csrf_token %}`
4. **Sesiones**: Configurables (30 días con "Recordarme", expiran al cerrar navegador sin marcar)
5. **HTTPS**: Recomendado para producción (SSL automático en Railway, Heroku, Render)

### OAuth con Google (Futuro)

Para implementar autenticación con Google OAuth:

1. Instalar `django-allauth`:
   ```bash
   pip install django-allauth
   ```

2. Configurar en `settings.py`:
   ```python
   INSTALLED_APPS += ['allauth', 'allauth.account', 'allauth.socialaccount', 'allauth.socialaccount.providers.google']
   ```

3. Configurar credenciales de Google Cloud Console

**Nota**: El sistema actual está preparado para esta integración futura.

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
  web: python3 manage.py collectstatic && python3 manage.py migrate && gunicorn proyecto.wsgi:application --workers 3 --log-file -
  ```
- **nixpacks.toml**: Configuración para Railway/Nixpacks (Python 3.13, PostgreSQL, MySQL)
- **runtime.txt**: Especifica Python 3.13.0
- **WhiteNoise**: Configurado para servir archivos estáticos sin nginx

### Despliegue en Railway (Recomendado)

Railway utiliza Nixpacks para construir y desplegar la aplicación automáticamente.

**Configuración `nixpacks.toml`:**
- Instala Python 3.13, PostgreSQL 16, MySQL 8.0
- Crea entorno virtual aislado (venv)
- Configura compilación de mysqlclient con MariaDB Connector/C
- Ejecuta collectstatic, migrate y gunicorn automáticamente

**Proceso de despliegue:**

1. **Conectar repositorio a Railway:**
   - Crear nuevo proyecto en Railway
   - Conectar repositorio Git (GitHub/GitLab)
   - Railway detectará automáticamente `nixpacks.toml`

2. **Configurar variables de entorno en Railway:**
   ```bash
   IS_DEPLOYED=True
   SECRET_KEY=clave-secreta-segura-generada
   DATABASE_SELECTOR=postgresql  # o mysql
   POSTGRESQL_DATABASE_URL=${RAILWAY_POSTGRESQL_URL}  # Auto-generada por Railway
   # O para MySQL:
   # MYSQL_DATABASE_URL=${RAILWAY_MYSQL_URL}

   # Opcional: AWS S3 para archivos media
   AWS_ACCESS_KEY_ID=tu-access-key
   AWS_SECRET_ACCESS_KEY=tu-secret-key
   AWS_STORAGE_BUCKET_NAME=tu-bucket
   AWS_S3_REGION_NAME=us-east-1
   ```

3. **Railway ejecutará automáticamente:**
   - Build de la imagen con Nixpacks
   - Instalación de dependencias en entorno virtual
   - Recolección de archivos estáticos
   - Migraciones de base de datos
   - Inicio del servidor Gunicorn

4. **Acceder a la aplicación:**
   - Railway proporcionará una URL pública automáticamente
   - Ejemplo: `https://tu-proyecto.up.railway.app`

**Características de Railway:**
- ✅ PostgreSQL/MySQL incluido y auto-configurado
- ✅ Builds automáticos en cada push
- ✅ Logs en tiempo real
- ✅ Variables de entorno encriptadas
- ✅ Escalado horizontal automático
- ✅ SSL/HTTPS incluido

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

- **Railway** ⭐ (Recomendado): PostgreSQL/MySQL, Nixpacks, builds automáticos
- **Heroku**: PostgreSQL incluido, fácil despliegue con Git
- **Render**: PostgreSQL gratuito, builds automáticos
- **DigitalOcean App Platform**: Flexible y escalable
- **AWS Elastic Beanstalk**: Infraestructura AWS completa

### Proceso de Despliegue (Plataformas Genéricas)

1. Conectar repositorio Git a la plataforma
2. Configurar variables de entorno
3. La plataforma ejecutará automáticamente los comandos del Procfile o nixpacks.toml
4. Acceder a la URL proporcionada por la plataforma

### Troubleshooting en Railway

Si el despliegue falla, revisa los logs en Railway:

**Error: "mysqlclient no compila"**
- Verifica que `nixpacks.toml` tenga `mariadb-connector-c` en nixPkgs
- Verifica que PKG_CONFIG_PATH esté configurado correctamente

**Error: "No module named pip"**
- El archivo `nixpacks.toml` usa venv, esto no debería ocurrir
- Verifica que la fase de install esté configurada correctamente

**Error: "externally-managed-environment"**
- El archivo `nixpacks.toml` usa venv para evitar este error
- No modifiques la instalación de paquetes fuera del venv

**Error: Build timeout**
- Verifica que requirements.txt no tenga dependencias innecesarias
- Railway tiene un timeout de 10 minutos por defecto

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
