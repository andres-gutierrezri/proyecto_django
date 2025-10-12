# WARP.md

Este archivo proporciona orientación a WARP (warp.dev) cuando trabaja con código en este repositorio.

Descripción del proyecto
- Framework: Django 5.x
- Estructura: Proyecto Django único (proyecto) con una app (app_1)
- Base de datos predeterminada: SQLite (el conector MySQL está presente en requirements pero no configurado)
- Idioma/localización: es-co, Zona horaria America/Bogota

Comandos comunes
- Entorno
  - Crear entorno virtual:
    ```bash
    # Windows
    python -m venv .venv && .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv && source .venv/bin/activate
    ```
  - Instalar dependencias:
    ```bash
    pip install -r requirements.txt --no-cache-dir
    ```
  - Scripts de inicio automático (recomendado):
    ```bash
    # Windows
    start_server.bat

    # macOS/Linux
    ./start_server.sh

    # Multiplataforma (Python)
    python start_server.py      # Windows
    python3 start_server.py     # macOS/Linux
    ```

- Ejecución
  - Aplicar migraciones:
    ```bash
    python manage.py migrate    # Windows
    python3 manage.py migrate   # macOS/Linux
    ```
  - Iniciar servidor de desarrollo:
    ```bash
    python manage.py runserver  # Windows
    python3 manage.py runserver # macOS/Linux
    ```
  - Verificaciones del sistema (lint ligero para configuración Django):
    ```bash
    python manage.py check      # Windows
    python3 manage.py check     # macOS/Linux
    ```

- Pruebas (ejecutor de pruebas de Django)
  - Ejecutar todas las pruebas:
    ```bash
    python manage.py test       # Windows
    python3 manage.py test      # macOS/Linux
    ```
  - Ejecutar pruebas para una sola app:
    ```bash
    python manage.py test app_1   # Windows
    python3 manage.py test app_1  # macOS/Linux
    ```
  - Ejecutar una sola prueba (módulo/clase/método):
    ```bash
    # ejemplos
    python manage.py test app_1.tests                           # Windows
    python3 manage.py test app_1.tests                          # macOS/Linux
    python manage.py test app_1.tests:SomeTestCase              # Windows
    python3 manage.py test app_1.tests:SomeTestCase             # macOS/Linux
    python manage.py test app_1.tests:SomeTestCase.test_something   # Windows
    python3 manage.py test app_1.tests:SomeTestCase.test_something  # macOS/Linux
    ```

- Usuario administrador (opcional):
  ```bash
  python manage.py createsuperuser    # Windows
  python3 manage.py createsuperuser   # macOS/Linux
  ```

- Archivos estáticos (desarrollo): servidos automáticamente desde app_1/static cuando DEBUG=True. No se requiere acción.

Arquitectura de alto nivel
- Proyecto (proyecto)
  - settings.py
    - DEBUG=True por defecto; ALLOWED_HOSTS incluye 127.0.0.1 y localhost
    - DATABASES: sqlite3 en BASE_DIR/db.sqlite3
    - Aplicaciones instaladas incluyen app_1
    - Archivos estáticos
      - STATIC_URL="/static/"
      - STATIC_ROOT=BASE_DIR / "staticfiles"
      - STATICFILES_DIRS incluye BASE_DIR / "app_1/static"
    - I18N/L10N/TZ configurado para español (Colombia) y America/Bogota
  - urls.py
    - Incluye URLConf de app_1 en la raíz
    - Admin en /admin/
  - wsgi.py como punto de entrada para despliegue

- Aplicación (app_1)
  - urls.py: mapea path("app_1/", views.app_1, name="app_1")
  - views.py: una vista de función simple que renderiza templates/index.html
  - templates/index.html
    - Carga recursos estáticos (css/styles.css, js/script.js, img/logo.png)
  - static/
    - css/styles.css, js/script.js, img/logo.png
  - models.py, admin.py, tests.py: actualmente son marcadores de posición mínimos

Comportamiento en tiempo de ejecución
- Enrutamiento inicial: El URLConf a nivel de proyecto incluye app_1.urls en la raíz, y app_1.urls expone la ruta "app_1/". Visita http://127.0.0.1:8000/app_1/ para ver el template index renderizado por views.app_1.
- Admin: http://127.0.0.1:8000/admin/ (crea un superusuario primero si es necesario).

Notas sobre la base de datos
- BD activa: SQLite vía django.db.backends.sqlite3 en settings.py.
- MySQL: mysql-connector-python está presente en requirements.txt pero no se usa. Para cambiar, actualiza settings.DATABASES para usar django.db.backends.mysql y proporciona NAME, USER, PASSWORD, HOST y PORT. Asegúrate de que el servidor MySQL y las credenciales existan antes de migrar.

Diferencias entre plataformas
- Windows: Usa `python`, `.venv\Scripts\activate`, ejecutable `python.exe`
- macOS/Linux: Usa `python3`, `source .venv/bin/activate`, ejecutable `python` o `python3`
- Scripts de inicio: `start_server.bat` (Windows), `start_server.sh` (macOS/Linux), `start_server.py` (multiplataforma)

Documentación y reglas
- README.md contiene orientación sobre configuración del entorno (versión de Python, venv, uso de pip) e instrucciones de ejecución (migrate, runserver). Consúltalo para pasos de configuración extendidos.
- CLAUDE.md proporciona orientación detallada para Claude Code sobre arquitectura del proyecto y comandos de desarrollo.
- No se encontraron archivos de reglas de Cursor/Copilot o flujos de trabajo CI.
