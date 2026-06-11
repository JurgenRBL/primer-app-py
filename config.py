
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Firebase
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
FIREBASE_MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID", "")

# Configuración de Firebase para Pyrebase
FIREBASE_CONFIG = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": FIREBASE_AUTH_DOMAIN,
    "projectId": FIREBASE_PROJECT_ID,
    "storageBucket": FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": FIREBASE_MESSAGING_SENDER_ID,
    "appId": FIREBASE_APP_ID,
    "databaseURL": ""  # No es necesario para Authentication
}

# Configuración de Airtable
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN", "")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "")
AIRTABLE_TABLE_PRODUCTOS = os.getenv("AIRTABLE_TABLE_PRODUCTOS", "Productos")
AIRTABLE_TABLE_USUARIOS = os.getenv("AIRTABLE_TABLE_USUARIOS", "Usuarios")

# Colores de la aplicación
COLOR_PRIMARIO = "#1E88E5"
COLOR_SECUNDARIO = "#42A5F5"
COLOR_ACENTO = "#90CAF9"
COLOR_FONDO = "#F5F7FA"
COLOR_TARJETA = "#FFFFFF"
COLOR_TEXTO = "#2C3E50"
COLOR_TEXTO_CLARO = "#7F8C8D"
COLOR_EXITO = "#4CAF50"
COLOR_ERROR = "#F44336"
COLOR_ADVERTENCIA = "#FF9800"

