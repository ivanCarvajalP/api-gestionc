from fastapi import FastAPI
from src.core.config import settings
from src.db import base

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
    
)

# para iniciar el servidor
# uvicorn src.main:app --reload


# para hacer migraciones
# alembic revision --autogenerate -m 'mesaje migracion'

# para aplicar las migraciones
# alembic upgrade head

# para revertir las migraciones
# alembic downgrade -1

