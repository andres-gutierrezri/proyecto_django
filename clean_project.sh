#!/bin/bash

################################################################
# SCRIPT DE LIMPIEZA COMPLETA DEL PROYECTO DJANGO
################################################################
# Este script realiza las siguientes tareas:
# 1. Elimina todas las migraciones del proyecto
# 2. Elimina y recrea la base de datos MySQL
# 3. Elimina el entorno virtual de Python
################################################################

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # Sin color

echo "================================================================"
echo "LIMPIEZA COMPLETA DEL PROYECTO DJANGO"
echo "================================================================"
echo ""

# ================================================================
# FUNCIÓN: Mostrar menú de opciones
# ================================================================
show_menu() {
    echo -e "${CYAN}Seleccione las tareas a realizar:${NC}"
    echo ""
    echo -e "${YELLOW}1)${NC} Eliminar migraciones"
    echo -e "${YELLOW}2)${NC} Eliminar y recrear base de datos MySQL"
    echo -e "${YELLOW}3)${NC} Eliminar entorno virtual de Python"
    echo -e "${YELLOW}4)${NC} Eliminar carpeta staticfiles"
    echo -e "${YELLOW}5)${NC} Ejecutar todas las tareas (1 + 2 + 3 + 4)"
    echo -e "${YELLOW}6)${NC} Salir"
    echo ""
}

# ================================================================
# FUNCIÓN: Eliminar migraciones
# ================================================================
delete_migrations() {
    echo ""
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}TAREA 1: ELIMINAR MIGRACIONES${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Contador de archivos eliminados
    py_count=0
    pyc_count=0
    
    echo -e "${YELLOW}🔍 Buscando archivos de migraciones...${NC}"
    echo ""
    
    # Buscar y contar archivos .py (excepto __init__.py)
    py_files=$(find . -path "*/migrations/*.py" -not -name "__init__.py" 2>/dev/null)
    if [ ! -z "$py_files" ]; then
        py_count=$(echo "$py_files" | wc -l | tr -d ' ')
    fi
    
    # Buscar y contar archivos .pyc
    pyc_files=$(find . -path "*/migrations/*.pyc" 2>/dev/null)
    if [ ! -z "$pyc_files" ]; then
        pyc_count=$(echo "$pyc_files" | wc -l | tr -d ' ')
    fi
    
    echo -e "${BLUE}📊 Archivos encontrados:${NC}"
    echo -e "   ${YELLOW}→${NC} Archivos .py de migraciones: ${YELLOW}${py_count}${NC}"
    echo -e "   ${YELLOW}→${NC} Archivos .pyc compilados: ${YELLOW}${pyc_count}${NC}"
    echo ""
    
    if [ $py_count -eq 0 ] && [ $pyc_count -eq 0 ]; then
        echo -e "${GREEN}✅ No hay archivos de migraciones para eliminar.${NC}"
        return 0
    fi
    
    # Pedir confirmación antes de eliminar
    echo -e "${YELLOW}⚠️  Se encontraron archivos de migraciones para eliminar.${NC}"
    echo ""
    read -p "$(echo -e ${YELLOW}¿Desea continuar con la eliminación? \(s/n\): ${NC})" confirmacion
    if [ "$confirmacion" != "s" ] && [ "$confirmacion" != "S" ]; then
        echo -e "${YELLOW}❌ Operación cancelada.${NC}"
        return 0
    fi
    echo ""
    
    # Eliminar archivos .py de migraciones (excepto __init__.py)
    if [ $py_count -gt 0 ]; then
        echo -e "${YELLOW}→${NC} Eliminando archivos .py..."
        find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        echo -e "${GREEN}✅ ${py_count} archivos .py eliminados${NC}"
    fi
    
    # Eliminar archivos .pyc de migraciones
    if [ $pyc_count -gt 0 ]; then
        echo -e "${YELLOW}→${NC} Eliminando archivos .pyc..."
        find . -path "*/migrations/*.pyc" -delete
        echo -e "${GREEN}✅ ${pyc_count} archivos .pyc eliminados${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Migraciones eliminadas exitosamente.${NC}"
}

# ================================================================
# FUNCIÓN: Recrear base de datos MySQL
# ================================================================
recreate_database() {
    echo ""
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}TAREA 2: RECREAR BASE DE DATOS MYSQL${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Cargar variables de entorno desde .env
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ Error: No se encontró el archivo .env${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📁 Cargando variables de entorno desde .env...${NC}"
    
    # Leer variables del archivo .env de forma más robusta
    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Ignorar líneas vacías y comentarios
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        
        # Eliminar espacios en blanco, comillas y caracteres de nueva línea
        key=$(echo "$key" | xargs | tr -d '\r\n')
        value=$(echo "$value" | xargs | tr -d "'\"\r\n")
        
        # Exportar solo las variables de MySQL necesarias
        case "$key" in
            MYSQL_DB_NAME|MYSQL_DB_USER|MYSQL_DB_PASSWORD|MYSQL_DB_HOST|MYSQL_DB_PORT)
                export "$key=$value"
                ;;
        esac
    done < .env
    
    # Verificar que las variables necesarias están definidas
    if [ -z "$MYSQL_DB_NAME" ] || [ -z "$MYSQL_DB_USER" ] || [ -z "$MYSQL_DB_PASSWORD" ] || [ -z "$MYSQL_DB_HOST" ] || [ -z "$MYSQL_DB_PORT" ]; then
        echo -e "${RED}❌ Error: Faltan variables de entorno necesarias en .env${NC}"
        echo -e "${YELLOW}   Variables requeridas: MYSQL_DB_NAME, MYSQL_DB_USER, MYSQL_DB_PASSWORD, MYSQL_DB_HOST, MYSQL_DB_PORT${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Variables de entorno cargadas correctamente${NC}"
    echo ""
    echo -e "${BLUE}📊 Configuración de la base de datos:${NC}"
    echo -e "   ${YELLOW}→${NC} Nombre: ${YELLOW}${MYSQL_DB_NAME}${NC}"
    echo -e "   ${YELLOW}→${NC} Usuario: ${YELLOW}${MYSQL_DB_USER}${NC}"
    echo -e "   ${YELLOW}→${NC} Host: ${YELLOW}${MYSQL_DB_HOST}${NC}"
    echo -e "   ${YELLOW}→${NC} Puerto: ${YELLOW}${MYSQL_DB_PORT}${NC}"
    echo ""
    
    # Verificar si la base de datos existe
    echo -e "${YELLOW}🔍 Verificando existencia de la base de datos...${NC}"
    
    db_check=$(mysql -u"$MYSQL_DB_USER" -p"$MYSQL_DB_PASSWORD" -h"$MYSQL_DB_HOST" -P"$MYSQL_DB_PORT" -e "SHOW DATABASES LIKE '${MYSQL_DB_NAME}';" 2>/dev/null | grep -v "Database")
    
    if [ ! -z "$db_check" ]; then
        echo -e "${GREEN}✅ Base de datos '${MYSQL_DB_NAME}' encontrada${NC}"
        echo ""
        
        echo -e "${YELLOW}🗑️  Eliminando base de datos existente...${NC}"
        
        # Comando SQL para eliminar la base de datos
        mysql -u"$MYSQL_DB_USER" -p"$MYSQL_DB_PASSWORD" -h"$MYSQL_DB_HOST" -P"$MYSQL_DB_PORT" -e "DROP DATABASE IF EXISTS \`${MYSQL_DB_NAME}\`;" 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Base de datos eliminada exitosamente${NC}"
        else
            echo -e "${RED}❌ Error al eliminar la base de datos${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  La base de datos '${MYSQL_DB_NAME}' no existe${NC}"
        echo -e "${BLUE}ℹ️  Se creará una nueva base de datos${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}🔨 Creando nueva base de datos...${NC}"
    
    # Comando SQL para crear la base de datos
    mysql -u"$MYSQL_DB_USER" -p"$MYSQL_DB_PASSWORD" -h"$MYSQL_DB_HOST" -P"$MYSQL_DB_PORT" -e "CREATE DATABASE \`${MYSQL_DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Base de datos creada exitosamente${NC}"
    else
        echo -e "${RED}❌ Error al crear la base de datos${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ Base de datos '${MYSQL_DB_NAME}' recreada exitosamente.${NC}"
}

# ================================================================
# FUNCIÓN: Eliminar entorno virtual
# ================================================================
delete_virtualenv() {
    echo ""
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}TAREA 3: ELIMINAR ENTORNO VIRTUAL${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}⚠️  El entorno virtual no existe (.venv)${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}🗑️  Eliminando entorno virtual...${NC}"
    
    # Eliminar el directorio del entorno virtual
    rm -rf .venv
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Entorno virtual eliminado exitosamente${NC}"
    else
        echo -e "${RED}❌ Error al eliminar el entorno virtual${NC}"
        return 1
    fi
}

# ================================================================
# FUNCIÓN: Eliminar carpeta staticfiles
# ================================================================
delete_staticfiles() {
    echo ""
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}TAREA 4: ELIMINAR CARPETA STATICFILES${NC}"
    echo -e "${MAGENTA}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ ! -d "staticfiles" ]; then
        echo -e "${YELLOW}⚠️  La carpeta staticfiles no existe${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}🗑️  Eliminando carpeta staticfiles...${NC}"
    
    # Eliminar el directorio staticfiles
    rm -rf staticfiles
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Carpeta staticfiles eliminada exitosamente${NC}"
    else
        echo -e "${RED}❌ Error al eliminar la carpeta staticfiles${NC}"
        return 1
    fi
}

# ================================================================
# FUNCIÓN: Mostrar instrucciones finales
# ================================================================
show_final_instructions() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}INSTRUCCIONES PARA CONTINUAR${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}📝 Próximos pasos recomendados:${NC}"
    echo ""
    echo -e "${BLUE}1. Recrear el entorno virtual:${NC}"
    echo -e "   ${YELLOW}python3 -m venv .venv${NC}"
    echo -e "   ${YELLOW}source .venv/bin/activate${NC}"
    echo -e "   ${YELLOW}pip install -r requirements.txt${NC}"
    echo ""
    echo -e "${BLUE}2. Crear las migraciones:${NC}"
    echo -e "   ${YELLOW}python manage.py makemigrations${NC}"
    echo -e "   ${YELLOW}python manage.py migrate${NC}"
    echo ""
    echo -e "${BLUE}3. Crear el superusuario:${NC}"
    echo -e "   ${YELLOW}python create_default_superuser.py${NC}"
    echo ""
    echo -e "${BLUE}4. Recolectar archivos estáticos:${NC}"
    echo -e "   ${YELLOW}python manage.py collectstatic --noinput${NC}"
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
}

# ================================================================
# PROGRAMA PRINCIPAL
# ================================================================
main() {
    while true; do
        show_menu
        read -p "$(echo -e ${YELLOW}Seleccione una opción \[1-6\]: ${NC})" opcion
        
        case $opcion in
            1)
                delete_migrations
                ;;
            2)
                echo ""
                echo -e "${RED}⚠️  ADVERTENCIA: Esta acción eliminará y recreará la base de datos.${NC}"
                echo -e "${RED}   TODOS los datos se perderán de forma permanente.${NC}"
                echo ""
                read -p "$(echo -e ${YELLOW}¿Desea continuar? \(s/n\): ${NC})" confirmacion
                if [ "$confirmacion" = "s" ] || [ "$confirmacion" = "S" ]; then
                    recreate_database
                else
                    echo -e "${YELLOW}❌ Operación cancelada.${NC}"
                fi
                ;;
            3)
                echo ""
                echo -e "${RED}⚠️  ADVERTENCIA: Esta acción eliminará el entorno virtual.${NC}"
                echo ""
                read -p "$(echo -e ${YELLOW}¿Desea continuar? \(s/n\): ${NC})" confirmacion
                if [ "$confirmacion" = "s" ] || [ "$confirmacion" = "S" ]; then
                    delete_virtualenv
                else
                    echo -e "${YELLOW}❌ Operación cancelada.${NC}"
                fi
                ;;
            4)
                echo ""
                echo -e "${RED}⚠️  ADVERTENCIA: Esta acción eliminará la carpeta staticfiles.${NC}"
                echo ""
                read -p "$(echo -e ${YELLOW}¿Desea continuar? \(s/n\): ${NC})" confirmacion
                if [ "$confirmacion" = "s" ] || [ "$confirmacion" = "S" ]; then
                    delete_staticfiles
                else
                    echo -e "${YELLOW}❌ Operación cancelada.${NC}"
                fi
                ;;
            5)
                echo ""
                echo -e "${RED}⚠️  ADVERTENCIA: Esta acción realizará las siguientes tareas:${NC}"
                echo -e "${RED}   1. Eliminar todas las migraciones${NC}"
                echo -e "${RED}   2. Eliminar y recrear la base de datos${NC}"
                echo -e "${RED}   3. Eliminar el entorno virtual${NC}"
                echo -e "${RED}   4. Eliminar carpeta staticfiles${NC}"
                echo -e "${RED}   TODOS los datos se perderán de forma permanente.${NC}"
                echo ""
                read -p "$(echo -e ${YELLOW}¿Desea continuar? \(s/n\): ${NC})" confirmacion
                if [ "$confirmacion" = "s" ] || [ "$confirmacion" = "S" ]; then
                    delete_migrations
                    recreate_database
                    delete_virtualenv
                    delete_staticfiles
                    show_final_instructions
                else
                    echo -e "${YELLOW}❌ Operación cancelada.${NC}"
                fi
                ;;
            6)
                echo ""
                echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Opción inválida. Por favor seleccione una opción del 1 al 6.${NC}"
                ;;
        esac
        
        echo ""
        read -p "$(echo -e ${CYAN}Presione ENTER para continuar...${NC})"
        clear
    done
}

# Limpiar pantalla y ejecutar programa principal
clear
main
