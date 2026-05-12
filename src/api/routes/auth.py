from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import psycopg2
from typing import List

from src.api.dependencies import get_db
#services
from src.services import usuario as usuario_service
#schemas
from src.schemas import usuario as usuario_schema
#security
from src.core.security import verify_password, create_access_token

router = APIRouter()

@router.post('/register', response_model=usuario_schema.UsuarioRegisterResponse)
def registrar_usuario(usuario: usuario_schema.UsuarioCreate, db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.registrar_usuario(db, usuario)


@router.post('/login', response_model=usuario_schema.UsuarioLoginResponse)
def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: psycopg2.extensions.connection = Depends(get_db)):
    """
    Login con OAuth2. En Swagger:
    - username = documento_identidad (ej: 111111)
    - password = contraseña
    """
    try:
        documento_identidad = int(form_data.username)
    except ValueError:
        raise HTTPException(status_code=422, detail="El documento de identidad debe ser un número")
    
    usuario = usuario_service.obtener_usuario_por_documento(documento_identidad, db)
    if not usuario or not verify_password(form_data.password, usuario["contrasena"]):
        raise HTTPException(status_code=401, detail="Documento o contraseña incorrectos")
    
    access_token = create_access_token(
        subject=usuario["documento_identidad"],
        extra_claims={"correo": usuario["correo"]}
    )
    
    response = usuario_schema.UsuarioLoginResponse(
        access_token=access_token,
        token_type="bearer",
        nombres=usuario["nombres"],
        correo=usuario["correo"],
        documento_identidad=usuario["documento_identidad"]
    )
    return response