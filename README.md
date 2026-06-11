
# Sistema de Gestión de Inventario CCTV

Aplicación de escritorio moderna desarrollada con Flet (Python), con autenticación Firebase y almacenamiento de datos en Airtable.

## Características

- ✅ Autenticación de usuarios con Firebase Authentication
- ✅ Gestión completa de productos (CRUD)
- ✅ Dashboard con estadísticas
- ✅ Búsqueda de productos
- ✅ Interfaz de usuario moderna y responsive
- ✅ Navegación elegante con NavigationRail
- ✅ Validaciones de formulario
- ✅ Snackbars y diálogos de confirmación
- ✅ Arquitectura modular (MVC)

## Estructura del Proyecto

```
Proyecto_CCTV/
├── main.py                 # Archivo principal de la aplicación
├── config.py              # Configuración y variables de entorno
├── requirements.txt       # Dependencias del proyecto
├── .env.example           # Ejemplo de variables de entorno
├── views/                 # Vistas de la aplicación
│   ├── login.py          # Vista de inicio de sesión
│   ├── dashboard.py      # Vista del dashboard
│   ├── productos.py      # Vista de gestión de productos
│   └── perfil.py         # Vista de perfil de usuario
├── services/              # Servicios
│   ├── firebase_auth.py  # Servicio de autenticación Firebase
│   └── airtable_service.py # Servicio de Airtable
├── models/                # Modelos de datos
│   └── producto.py       # Modelo de Producto
└── assets/               # Recursos (imágenes, iconos)
    └── iconos/
```

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de Firebase

1. Ir a la [Consola de Firebase](https://console.firebase.google.com/)
2. Crear un nuevo proyecto
3. Habilitar **Authentication** con correo y contraseña
4. Crear un usuario de prueba en la sección de Users
5. Ir a **Project Settings** > **General** y buscar la sección **Your apps**
6. Registrar una nueva app web y copiar la configuración (apiKey, authDomain, projectId, etc.)

## Configuración de Airtable

1. Crear una cuenta en [Airtable](https://airtable.com/)
2. Crear una nueva base de datos (Base)
3. Crear dos tablas:

   **Tabla: Productos**
   - Campos:
     - Nombre (Texto simple)
     - Descripción (Texto largo)
     - Fecha (Fecha)
     - Estado (Selección única: Disponible, Agotado, Descontinuado)
     - Precio (Número - Moneda)
     - Stock (Número)
     - Categoría (Texto simple)

   **Tabla: Usuarios**
   - Campos:
     - ID (Texto simple)
     - Nombre (Texto simple)
     - Correo (Correo electrónico)
     - Contraseña (Texto simple - solo para referencia)
     - Rol (Selección única: Administrador, Usuario)

4. Obtener el **Base ID**:
   - Abrir la base de datos y ver la URL: `https://airtable.com/appXXXXXXXXX/...`
   - El ID es la parte que empieza por `app`

5. Crear un **Personal Access Token**:
   - Ir a https://airtable.com/create/tokens
   - Crear un nuevo token con permisos de escritura y lectura para la base de datos

## Configuración del Proyecto

1. Copiar el archivo `.env.example` y renombrarlo a `.env`
2. Completar las variables de entorno en el archivo `.env`:
   ```env
   # Firebase
   FIREBASE_API_KEY=tu_api_key_aqui
   FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com
   FIREBASE_PROJECT_ID=tu_proyecto_id
   FIREBASE_STORAGE_BUCKET=tu_proyecto.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
   FIREBASE_APP_ID=tu_app_id

   # Airtable
   AIRTABLE_TOKEN=tu_token_de_personal_access
   AIRTABLE_BASE_ID=tu_base_id
   AIRTABLE_TABLE_PRODUCTOS=Productos
   AIRTABLE_TABLE_USUARIOS=Usuarios
   ```

## Ejecutar la Aplicación

```bash
python main.py
```

## Uso

1. Inicia sesión con el correo y contraseña del usuario que creaste en Firebase
2. En el **Dashboard** verás las estadísticas del inventario
3. En **Gestión de Datos** podrás agregar, editar y eliminar productos
4. En **Perfil** verás tu información y podrás cerrar sesión

## Tecnologías Utilizadas

- **Flet**: Framework para construir aplicaciones de escritorio, web y móviles
- **Pyrebase4**: Wrapper de Firebase para Python
- **PyAirtable**: Cliente de Airtable para Python
- **python-dotenv**: Para manejar variables de entorno

