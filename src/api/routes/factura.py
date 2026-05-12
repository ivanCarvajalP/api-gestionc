from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
import psycopg2
from src.services import factura_service
from src.crud import factura as factura_crud
from src.crud import servicio as servicio_crud
from src.crud import vehiculo as vehiculo_crud
from src.api.dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/upload")
async def register_factura(
    placa: str = Form(...),
    file: UploadFile = File(...),
    db: psycopg2.extensions.connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Subir una factura en formato PDF. Extrae la información, 
    valida en Groq, la aloja en Supabase y la persiste en BD.
    """
    resultado = await factura_service.save_factura(db=db, file=file, placa=placa)
    
    return {
        "status": "success",
        "message": "Factura subida y parseada correctamente",
        "data": resultado
    }


@router.get("/vehiculo/{placa}")
def obtener_facturas_por_vehiculo(
    placa: str,
    db: psycopg2.extensions.connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene todas las facturas de un vehículo con sus servicios/items asociados.
    """
    # Verificar que el vehículo existe
    vehiculo = vehiculo_crud.get_by_placa(db, placa)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    # Obtener facturas del vehículo
    facturas = factura_crud.find_by_placa(db, placa)
    
    # Para cada factura, obtener sus servicios
    resultado = []
    for factura in facturas:
        servicios = servicio_crud.find_by_factura(db, factura["id_factura"])
        factura["servicios"] = servicios
        resultado.append(factura)
    
    return {
        "placa": placa,
        "total_facturas": len(resultado),
        "facturas": resultado
    }

