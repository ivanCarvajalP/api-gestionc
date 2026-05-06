import psycopg2
from psycopg2.extras import RealDictCursor
from src.schemas.vehiculo import VehiculoCreate


def get_by_placa(db: psycopg2.extensions.connection, placa: str):
    """
    Busca un vehículo en la base de datos a partir de su placa.
    Retorna un diccionario con los datos del vehículo si existe, o None si no se encuentra.
    """
    query = "SELECT * FROM vehiculos WHERE placa = %(placa)s"
    
    with db.cursor() as cursor:
        cursor.execute(query, {"placa": placa})
        resultado = cursor.fetchone()

        return dict(resultado) if resultado else None


def insert_vehiculo(db: psycopg2.extensions.connection, vehiculo: VehiculoCreate):
    query = """
    INSERT INTO vehiculos 
    (placa, cilindraje, marca) 
    VALUES (
    %(placa)s,
    %(cilindraje)s,
    %(marca)s
    )
    ON CONFLICT (placa) DO NOTHING
    """

    with db.cursor() as cursor:
        cursor.execute(query, vehiculo.model_dump())
        # db.commit() handled by service
        return True
