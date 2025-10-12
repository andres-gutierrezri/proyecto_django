
# Proyecto: Ejemplo inicial para Django

## Requisitos
| Software | Versión recomendada |
|----------|--------------------|
| Python   | 3.10 o superior |
| Dependencias de Python | Ver `requirements.txt` |

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

## Instalación

# Habilitar la Ejecución de Scripts en PowerShell
```powershell
# Directiva de ejecución para el usuario actual
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force

# Comprobar la directiva de ejecución
# Debe mostrar Unrestricted
Get-ExecutionPolicy -List
```

# Verificar la instalación de Python y pip
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

# Instalar entorno virtual de Python
```bash
# Instalar entorno virtual de Python
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

# Instalar dependencias para el proyecto
```bash
# Comprobar la versión de pip
pip --version

# Instalar las dependencias del proyecto
pip install -r requirements.txt --no-cache-dir

# Verificar la instalación de dependencias
pip freeze

# Comprobar las dependencias instaladas con sus versiones
pip list

# Comprobar si hay actualizaciones disponibles
pip list --outdated

# Comprobar la versión de Django
django-admin --version
```

## Uso inicial (Ejecutar el proyecto)

### Método automático (recomendado)
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

Estos scripts automáticamente:
- Crean y activan el entorno virtual
- Verifican y reparan pip si es necesario
- Instalan las dependencias desde requirements.txt
- Ejecutan las migraciones de la base de datos
- Inician el servidor de desarrollo
- Abren el navegador en http://127.0.0.1:8000/

### Método manual
Para comenzar a trabajar con el proyecto, asegúrese de que el entorno virtual está activado y que ha instalado todas las dependencias necesarias. A continuación, puede ejecutar el proyecto Django, debe correr las siguientes instrucciones:

```bash
# Correr migraciones
python manage.py migrate

# Ejecutar el servidor de desarrollo
python manage.py runserver
```

## Control de versiones

```bash
git init
git add .
git commit -m "feat: Ejemplo inicial para Django"
git remote add origin https://github.com/USUARIO/proyecto.git
git push -u origin main
```

Para GitLab sustituya la URL de *remote*.

## Mensajes de Commit Recomendados

Para mantener un historial de commits claro y conciso, se recomiendan los siguientes formatos de mensaje:

*   **feat**: Nueva característica

---

© 2025 · Licencia MIT
