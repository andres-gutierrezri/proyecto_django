# -*- coding: utf-8 -*-

# Importar os para manejar las variables de entorno
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# Configuraciones para Amazon S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")

# Configuración de la URL del bucket
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Opcional: Configuración de ACL predeterminada
AWS_DEFAULT_ACL = "public-read"  # Asegura que los archivos sigan la ACL del bucket o no sean públicos por defecto
