from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.dependencies import get_db
from src.services import usuario as usuario_service
from src.schemas import usuario as usuario_schema

router = APIRouter()

@router.post('/register', response_model=usuario_schema.UsuarioResponse)
def registrar_usuario(usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.registrar_usuario(db, usuario)

@router.post('/login', response_model=usuario_schema.UsuarioLoginResponse)
def login_usuario(login : usuario_schema.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario_por_documento(login.documento_identidad, db)
    if not usuario or usuario["contrasena"] != login.contrasena:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    response = usuario_schema.UsuarioLoginResponse(
        acces_token="token_de_ejemplo",  # para el token
        token_type="bearer",
        nombres=usuario["nombres"],
        correo=usuario["correo"],
        documento_identidad=usuario["documento_identidad"]
    )
    return response