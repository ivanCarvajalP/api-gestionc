from fastapi import APIRouter, Depends
import psycopg2
from typing import List
from src.api.dependencies import get_db
from src.services import usuario as usuario_service
from src.schemas import usuario as usuario_schema


router = APIRouter()


@router.get('/', response_model=List[usuario_schema.UsuarioResponse])
def obtener_usuarios(db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.obtener_usuarios(db)


@router.get('/{documento_identidad}', response_model=usuario_schema.UsuarioResponse)
def obtener_usuario_por_documento(documento_identidad: int, db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.obtener_usuario_por_documento(documento_identidad, db)


@router.put('/{documento_identidad}', response_model=usuario_schema.UsuarioResponse)
def actualizar_usuario(documento_identidad: int, usuario: usuario_schema.UsuarioUpdate, db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.actualizar_usuario(documento_identidad, usuario, db)

@router.get('/{documento_identidad}/vehiculos')
def obtener_vehiculos_de_un_usuario(documento_identidad: int, db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.obtener_vehiculos_de_un_usuario(documento_identidad, db)


from src.schemas import vehiculo as vehiculo_schema

@router.post('/{documento_identidad}/vehiculos')
def registrar_vehiculo_usuario(documento_identidad: int, registro: vehiculo_schema.RegistroVehiculoUsuario, db: psycopg2.extensions.connection = Depends(get_db)):
    return usuario_service.registrar_vehiculo_usuario(documento_identidad, registro, db)

@router.delete('/{documento_identidad}/vehiculos/{placa}')
def eliminar_vehiculo_usuario(documento_identidad: int, placa: str, db: psycopg2.extensions.connection = Depends(get_db)):
    """Elimina de forma lógica un vehículo asociado a un usuario"""
    return usuario_service.eliminar_vehiculo_usuario(documento_identidad, placa, db)