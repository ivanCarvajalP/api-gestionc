# API Gestión

Este proyecto es una API desarrollada con **FastAPI**, que se conecta a una base de datos relacional en **PostgreSQL** y a un servidor de datos semánticos en **Apache Jena Fuseki**.

## Requisitos previos

Asegúrate de tener instalado y ejecutándose lo siguiente en tu sistema:
- [Python 3.x](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) (Requiere **Java 11** o superior)

## Instalación y Configuración

Sigue estos pasos para clonar el repositorio y ejecutar el proyecto localmente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Eliud-Garcia/api-gestion.git
cd api-gestion
```

### 2. Crear y activar el entorno virtual

Es recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**En Linux/macOS:**
```bash
python3 -m venv env
source env/bin/activate
```

**En Windows:**
```bash
python -m venv env
.\env\Scripts\activate
```

### 3. Instalar dependencias

Con el entorno virtual activado, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

El proyecto requiere variables de entorno para conectarse a las bases de datos. Crea un archivo `.env` a partir del archivo de ejemplo:

**En Linux/macOS:**
```bash
cp .env_example .env
```

**En Windows (Command Prompt):**
```cmd
copy .env_example .env
```

Abre el archivo `.env` y asegúrate de configurar correctamente los valores de conexión:

```env
DATABASE_URL=postgresql://user:password@host/db_name
FUSEKI_ENDPOINT_URL=http://localhost:3030/my_dataset/query
```

### 5. Aplicar migraciones de la base de datos

Este proyecto usa Alembic para gestionar las migraciones en PostgreSQL. Ejecuta el siguiente comando para crear las tablas en tu base de datos:

```bash
alembic upgrade head
```

### 6. Ejecutar el proyecto

Finalmente, para levantar el servidor de desarrollo con recarga automática, ejecuta:

```bash
uvicorn src.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`. 
Puedes acceder a la documentación interactiva provista por FastAPI en `http://127.0.0.1:8000/docs` o `http://127.0.0.1:8000/redoc`.
