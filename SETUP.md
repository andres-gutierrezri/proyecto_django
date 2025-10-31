# Configuración del Proyecto Django

Este documento describe el proceso de configuración inicial del proyecto para nuevos desarrolladores.

## Requisitos Previos

- Python 3.13.0 o superior
- MySQL o PostgreSQL (recomendado para producción)
- Git

## Pasos de Configuración

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd proyecto_django
```

### 2. Crear Entorno Virtual

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# Configuración general
SECRET_KEY=tu-clave-secreta-aqui
IS_DEPLOYED=False
DATABASE_SELECTOR=mysql  # o postgresql

# MySQL
MYSQL_DB_NAME=proyecto
MYSQL_DB_USER=root
MYSQL_DB_PASSWORD=tu-contraseña
MYSQL_DB_HOST=localhost
MYSQL_DB_PORT=3306

# PostgreSQL (alternativo)
POSTGRESQL_DB_NAME=proyecto
POSTGRESQL_DB_USER=postgres
POSTGRESQL_DB_PASSWORD=tu-contraseña
POSTGRESQL_DB_HOST=localhost
POSTGRESQL_DB_PORT=5432

# Email (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

### 5. Generar y Aplicar Migraciones

**IMPORTANTE:** Las migraciones NO están incluidas en el repositorio y se generan automáticamente.

```bash
# Generar archivos de migración para cambios en modelos
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

Esto creará automáticamente:
- `app_1/migrations/0002_usersession.py` - Tabla de sesiones de usuarios
- Todas las tablas necesarias en la base de datos

**Nota para Producción (Railway):**
En producción, el archivo `nixpacks.toml` está configurado para ejecutar automáticamente `makemigrations` y `migrate` durante cada despliegue, por lo que no es necesario incluir las migraciones en Git.

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa:
- Email
- Nombre de usuario
- Nombre
- Apellido
- Contraseña (mínimo 8 caracteres, con mayúscula, minúscula y carácter especial)

### 7. Ejecutar Servidor de Desarrollo

**Opción A - Script Automático (Recomendado):**

```bash
# macOS/Linux
./start_server.sh

# Windows
start_server.bat

# Python (multiplataforma)
python start_server.py
```

**Opción B - Manual:**

```bash
# macOS/Linux
python3 manage.py runserver 127.0.0.1:8000

# Windows
python manage.py runserver 127.0.0.1:8000
```

### 8. Acceder a la Aplicación

- **Aplicación:** http://127.0.0.1:8000/
- **Panel de Administración:** http://127.0.0.1:8000/admin/

## Características del Sistema

### Sistema de Autenticación
- Registro de usuarios con verificación de email
- Login con email (no username)
- Contraseñas seguras con validación estricta
- Restablecimiento de contraseña por email
- Notificaciones de inicio de sesión
- Emails condicionales según entorno (IS_DEPLOYED)
- Creación automática de superusuario en despliegue

### Gestión de Sesiones
- Rastreo de sesiones activas por usuario (modelo UserSession)
- Detección de múltiples dispositivos
- Cierre remoto de sesiones desde el dashboard
- Timeout automático después de 30 minutos de inactividad
- Limpieza automática de sesiones inválidas

### Sistema de Emails
- **Desarrollo (`IS_DEPLOYED=False`)**: Emails en consola (solo texto plano)
- **Producción (`IS_DEPLOYED=True`)**: Emails SMTP (texto plano + HTML)
- Control automático mediante variable IS_DEPLOYED
- Templates responsive con Bootstrap

### Dashboard
- Información de cuenta del usuario
- Visualización de sesiones activas con detalles
- Alertas de seguridad para múltiples sesiones
- Gestión de sesiones remotas (cerrar sesiones individuales)
- Información de dispositivos y última actividad
- Tema claro/oscuro

## Solución de Problemas

### Error: "No module named 'django'"
```bash
# Asegúrate de activar el entorno virtual
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Error: "django.db.utils.OperationalError"
- Verifica que MySQL/PostgreSQL esté ejecutándose
- Confirma las credenciales en el archivo `.env`
- Asegúrate de que la base de datos exista

### Error: "You have unapplied migrations"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error en envío de emails
- Para Gmail, genera una "Contraseña de aplicación"
- En desarrollo, usa `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

## Estructura del Proyecto

```
proyecto_django/
├── app_1/                      # Aplicación principal
│   ├── migrations/             # Migraciones (generadas localmente)
│   ├── templates/              # Plantillas HTML
│   ├── static/                 # Archivos estáticos (CSS, JS, imágenes)
│   ├── models.py               # Modelos de base de datos
│   ├── views.py                # Vistas
│   ├── forms.py                # Formularios
│   └── urls.py                 # URLs de la aplicación
├── proyecto/                   # Configuración del proyecto
│   ├── settings.py             # Configuración principal
│   ├── local_settings.py       # Configuración de BD
│   └── urls.py                 # URLs raíz
├── .env                        # Variables de entorno (NO en Git)
├── requirements.txt            # Dependencias Python
└── manage.py                   # Comando de gestión Django
```

## Notas Importantes

1. **Migraciones:** Se generan automáticamente con `makemigrations` en cada entorno
2. **Archivo .env:** NO está en Git, debe crearse manualmente
3. **Base de datos:** SQLite solo para desarrollo, usar MySQL/PostgreSQL en producción
4. **Sesiones:** Timeout configurado a 30 minutos de inactividad

## Contribuir

1. Crear una rama desde `develop`
2. Hacer cambios y commits
3. Ejecutar `makemigrations` si modificaste models.py
4. Probar localmente
5. Crear Pull Request a `develop`

## Soporte

Para problemas o preguntas, contactar al equipo de desarrollo.
