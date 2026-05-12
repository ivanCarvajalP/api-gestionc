import psycopg2
from psycopg2.extras import RealDictCursor

from src.schemas.servicio import ServicioCreate

def insert_servicio(db: psycopg2.extensions.connection, servicio: ServicioCreate):
    """
    Inserta un nuevo servicio en la base de datos.
    """

    query = """
    INSERT INTO servicios 
    (nombre, costo, cantidad, fk_idfactura)
    VALUES (%s, %s, %s, %s)
    RETURNING id_servicio
    """
    
    with db.cursor() as cursor:
        cursor.execute(query, (servicio.nombre, servicio.costo, servicio.cantidad, servicio.fk_idfactura))
        resultado = cursor.fetchone()
        db.commit()
        return resultado["id_servicio"] if resultado else None

def find_by_factura(db: psycopg2.extensions.connection, id_factura: str):
    """
    Obtiene todos los servicios asociados a una factura.
    """
    query = """
        SELECT id_servicio, nombre, costo, cantidad
        FROM servicios 
        WHERE fk_idfactura = %(id_factura)s
    """
    with db.cursor() as cursor:
        cursor.execute(query, {"id_factura": id_factura})
        resultados = cursor.fetchall()
        return [dict(row) for row in resultados]