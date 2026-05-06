from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional

#para crear un vehiculo
class VehiculoCreate(BaseModel):
    placa: str
    cilindraje: int
    marca: str

class VehiculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    placa: str
    cilindraje: int
    marca: str

class TarjetaPropiedadCreate(BaseModel):
    numero_tarjeta: int
    nombre_propietario: str
    documento_propietario: int
    clase_vehiculo: str
    modelo: str
    capacidad: int
    servicio: str
    tipo_carroceria: str
    linea_vehiculo: str
    numero_motor: str
    combustible: str
    color: str

class RegistroVehiculoUsuario(BaseModel):
    vehiculo: VehiculoCreate
    tarjeta_propiedad: TarjetaPropiedadCreate
    kilometros_registro: Optional[int] = 0