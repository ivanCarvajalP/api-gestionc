import psycopg2
from src.schemas.vehiculo import TarjetaPropiedadCreate

def insert_tarjeta_propiedad(db: psycopg2.extensions.connection, tarjeta: TarjetaPropiedadCreate, placa: str, cilindraje: int, marca: str):
    """
    Inserta una nueva tarjeta de propiedad.
    Recibe la placa, cilindraje y marca para rellenar los datos duplicados de la tabla.
    No hace commit, para mantener la atomicidad de la transacción.
    """
    query = """
    INSERT INTO tarjetapropiedad (
        numero_tarjeta, nombre_propietario, cilindraje, documento_propietario, 
        marca, clase_vehiculo, modelo, capacidad, servicio, tipo_carroceria, 
        linea_vehiculo, numero_motor, combustible, color, placa, fk_placavehiculo
    ) VALUES (
        %(numero_tarjeta)s, %(nombre_propietario)s, %(cilindraje)s, %(documento_propietario)s, 
        %(marca)s, %(clase_vehiculo)s, %(modelo)s, %(capacidad)s, %(servicio)s, %(tipo_carroceria)s, 
        %(linea_vehiculo)s, %(numero_motor)s, %(combustible)s, %(color)s, %(placa)s, %(fk_placavehiculo)s
    )
    """

    data = tarjeta.model_dump()
    data["placa"] = placa
    data["fk_placavehiculo"] = placa
    data["cilindraje"] = cilindraje
    data["marca"] = marca

    with db.cursor() as cursor:
        cursor.execute(query, data)
        return True
