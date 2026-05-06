from fastapi import HTTPException
from src.crud import vehiculo as vehiculo_crud

def get_by_placa(db: psycopg2.extensions.connection, placa: str):
    vehiculo = vehiculo_crud.get_by_placa(db, placa)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo