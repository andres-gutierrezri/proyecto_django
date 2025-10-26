# -*- coding: utf-8 -*-

import os
import dj_database_url
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# Variable para escoger la base de datos local o de producción
# Si IS_DEPLOYED es 'True', se escoge la base de datos de producción, de lo contrario, se escoge la base de datos local.
IS_DEPLOYED = os.getenv("IS_DEPLOYED", "False") == "True"

# Variable para escoger la base de datos a utilizar
# Si DATABASE_SELECTOR es 'postgresql', se escoge la base de datos PostgreSQL
# Si DATABASE_SELECTOR es 'mysql', se escoge la base de datos MySQL
DATABASE_SELECTOR = os.getenv("DATABASE_SELECTOR", "postgresql")

# Si DATABASE_SELECTOR no es 'postgresql' o 'mysql', se establece en 'postgresql'
if DATABASE_SELECTOR != "postgresql" and DATABASE_SELECTOR != "mysql":
    DATABASE_SELECTOR = "postgresql"
else:
    pass # No hacer nada si DATABASE_SELECTOR es 'postgresql' o 'mysql'

# Configuración de la base de datos
if DATABASE_SELECTOR == "postgresql":
    if IS_DEPLOYED:
        DATABASE_DICT = dj_database_url.config(default=os.getenv("POSTGRESQL_DATABASE_URL"))
    else:
        DATABASE_DICT = {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRESQL_DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRESQL_DB_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRESQL_DB_PASSWORD", ""),
            "HOST": os.getenv("POSTGRESQL_DB_HOST", "localhost"),
            "PORT": os.getenv("POSTGRESQL_DB_PORT", "5432"),
            "OPTIONS": {
                "client_encoding": "UTF8",
            },
            "TEST": {
                "NAME": os.getenv("POSTGRESQL_DB_TEST", "test"),
            },
        }
elif DATABASE_SELECTOR == "mysql":
    if IS_DEPLOYED:
        DATABASE_DICT = dj_database_url.config(default=os.getenv("MYSQL_DATABASE_URL"))
    else:
        DATABASE_DICT = {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DB_NAME", "mysql"),
            "USER": os.getenv("MYSQL_DB_USER", "root"),
            "PASSWORD": os.getenv("MYSQL_DB_PASSWORD", ""),
            "HOST": os.getenv("MYSQL_DB_HOST", "localhost"),
            "PORT": os.getenv("MYSQL_DB_PORT", "3306"),
            "OPTIONS": {
                "sql_mode": "traditional",
                "charset": "utf8mb4",
                "init_command": "SET default_storage_engine=INNODB",
            },
            "TEST": {
                "NAME": os.getenv("MYSQL_DB_TEST", "test"),
            },
        }
else:
    print(
        "Error: DATABASE SELECTOR debe ser 'postgresql' o 'mysql'.\n"
        + "Se utiliza el valor predeterminado 'postgresql'.\n"
        + "Establezca la variable de entorno DATABASE SELECTOR en 'postgresql' o 'mysql' antes de ejecutar el servidor."
    )
