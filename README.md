# 🚗 API Mi Vehículo

API REST para la gestión integral de vehículos, facturas y usuarios. Desarrollada con **FastAPI** (Python), respaldada por **PostgreSQL** para datos relacionales y **Apache Jena Fuseki** para consultas semánticas SPARQL sobre una ontología OWL.

## 📋 Descripción

Esta API permite:

- **Gestión de usuarios**: Registro, autenticación JWT, consulta y actualización de perfiles.
- **Gestión de vehículos**: Registro de vehículos con tarjeta de propiedad, asociación a usuarios y baja lógica.
- **Procesamiento de facturas**: Carga de PDFs de facturas, extracción automática de datos con `pdfplumber`, clasificación inteligente de productos/servicios con IA (Groq LLaMA 3.3) y almacenamiento en Supabase Storage.
- **Consultas semánticas**: Consultas SPARQL a una ontología OWL cargada en Apache Jena Fuseki, para explorar relaciones entre usuarios, vehículos, facturas y servicios.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│              Contenedor Docker                  │
│                                                 │
│  ┌──────────────┐      ┌──────────────────┐     │
│  │   FastAPI     │      │  Apache Jena     │     │
│  │   (uvicorn)   │─────▶│  Fuseki :3030    │     │
│  │   :PORT       │SPARQL│  (TDB2 + .ttl)   │     │
│  └──────┬───────┘      └──────────────────┘     │
│         │                                       │
└─────────┼───────────────────────────────────────┘
          │
    ┌─────┼──────────────────────┐
    │     │                      │
    ▼     ▼                      ▼
PostgreSQL  Supabase Storage   Groq AI
 (Railway)   (PDFs facturas)   (LLaMA 3.3)
```

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Framework API | FastAPI + Uvicorn |
| Base de datos relacional | PostgreSQL (psycopg2) |
| Base de datos semántica | Apache Jena Fuseki (SPARQL + TDB2) |
| Autenticación | JWT (python-jose + passlib) |
| Procesamiento de PDFs | pdfplumber |
| Clasificación IA | Groq (LLaMA 3.3 70B) |
| Almacenamiento de archivos | Supabase Storage |
| Contenerización | Docker + supervisord |
| Despliegue | Railway |

## 📡 Endpoints

### Autenticación (`/api/auth`)

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/auth/register` | Registrar un nuevo usuario |
| `POST` | `/api/auth/login` | Iniciar sesión (devuelve token JWT) |

### Usuarios (`/api/usuarios`) 🔒

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/usuarios/{doc}` | Obtener usuario por documento |
| `PUT` | `/api/usuarios/{doc}` | Actualizar datos de usuario |
| `GET` | `/api/usuarios/{doc}/vehiculos` | Vehículos de un usuario |
| `POST` | `/api/usuarios/{doc}/vehiculos` | Registrar vehículo a un usuario |
| `DELETE` | `/api/usuarios/{doc}/vehiculos/{placa}` | Dar de baja un vehículo |

### Facturas (`/api/facturas`) 🔒

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/facturas/upload` | Subir factura PDF (extrae datos automáticamente) |
| `GET` | `/api/facturas/vehiculo/{placa}` | Facturas de un vehículo con sus servicios |

### Ontología Semántica (`/api/semantica`) 🔒

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/semantica/usuarios-vehiculos` | Usuarios y sus vehículos (SPARQL) |
| `GET` | `/api/semantica/usuarios/{doc}/vehiculos` | Vehículos de un usuario (SPARQL) |
| `GET` | `/api/semantica/facturas-vehiculos` | Facturas y sus vehículos (SPARQL) |
| `GET` | `/api/semantica/vehiculos/{placa}/servicios` | Servicios de un vehículo (SPARQL) |

> 🔒 Los endpoints marcados requieren autenticación Bearer Token (JWT).

## 🚀 Inicio Rápido con Docker (Recomendado)

La forma más sencilla de ejecutar el proyecto completo (API + Fuseki) es con Docker.

### Requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado y ejecutándose.

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Eliud-Garcia/api-gestion.git
   cd api-gestion
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env_example .env
   ```
   Edita el archivo `.env` con tus credenciales:
   ```env
   DATABASE_URL=postgresql://user:password@host/db_name
   FUSEKI_ENDPOINT_URL=http://localhost:3030/vehiculo/query
   SECRET_KEY=TU_SECRET_KEY_MUY_LARGA_Y_DIFICIL_AQUI
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GROQ_API_KEY=TU_API_KEY_AQUI
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=SERVICE_ROL_SECRET
   SUPABASE_BUCKET=SUPABASE_BUCKET_NAME
   ```

3. **Construir e iniciar**
   ```bash
   docker compose up --build
   ```

4. **Acceder a la API**
   - API: `http://localhost:8000`
   - Documentación Swagger: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

> El contenedor incluye Apache Jena Fuseki con la ontología precargada automáticamente. No se necesita configuración adicional.

## 💻 Instalación Local (Sin Docker)

Si prefieres ejecutar sin Docker, necesitarás instalar cada componente manualmente.

### Requisitos previos

- [Python 3.12+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) (requiere Java 11+)

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Eliud-Garcia/api-gestion.git
   cd api-gestion
   ```

2. **Crear y activar entorno virtual**

   **Linux/macOS:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env_example .env
   ```
   Edita `.env` con tus credenciales (ver sección anterior).

5. **Configurar la base de datos**

   Ejecuta el script SQL en tu servidor PostgreSQL para crear las tablas:
   ```bash
   psql -U tu_usuario -d tu_base_de_datos -f database/tables.sql
   ```

6. **Iniciar Apache Jena Fuseki**

   Descarga Fuseki, crea un dataset llamado `vehiculo` y carga la ontología:
   ```bash
   # Iniciar Fuseki
   ./fuseki-server --port=3030

   # En otro terminal, cargar la ontología
   ./tdb2.tdbloader --loc=/ruta/al/dataset ontologia/ontologia.ttl
   ```

7. **Ejecutar la API**
   ```bash
   uvicorn src.main:app --reload
   ```

   La API estará en `http://127.0.0.1:8000`.

## 🗄️ Estructura del Proyecto

```
api-gestionc/
├── src/
│   ├── main.py                 # Punto de entrada de FastAPI
│   ├── api/
│   │   ├── dependencies.py     # Inyección de dependencias (DB, Auth)
│   │   └── routes/             # Endpoints de la API
│   │       ├── auth.py         # Login y registro
│   │       ├── factura.py      # Upload y consulta de facturas
│   │       ├── semantic.py     # Consultas SPARQL
│   │       └── usuario.py      # CRUD de usuarios y vehículos
│   ├── core/
│   │   ├── config.py           # Configuración (pydantic-settings)
│   │   └── security.py         # JWT y hashing de contraseñas
│   ├── crud/                   # Queries SQL directas (psycopg2)
│   ├── db/
│   │   ├── connection.py       # Conexión PostgreSQL
│   │   └── semantic.py         # Conexión a Fuseki (rdflib)
│   ├── schemas/                # DTOs (Pydantic models)
│   └── services/               # Lógica de negocio
│       ├── factura_service.py  # Procesamiento de PDFs
│       ├── groq_service.py     # Clasificación IA de productos
│       └── supabase_service.py # Almacenamiento de PDFs
├── ontologia/
│   └── ontologia.ttl           # Ontología OWL (usuarios, vehículos, facturas)
├── database/
│   └── tables.sql              # Script de creación de tablas
├── Dockerfile                  # Contenedor con Python + Java + Fuseki
├── docker-compose.yml          # Orquestación local
├── supervisord.conf            # Gestión de procesos (Fuseki + API)
├── start.sh                    # Script de inicio del contenedor
├── fuseki-config.ttl           # Configuración del dataset Fuseki
├── requirements.txt            # Dependencias Python
└── .env_example                # Plantilla de variables de entorno
```


## 📄 Licencia

Este proyecto es de uso académico.
