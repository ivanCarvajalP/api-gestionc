from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from src.db.base_class import Base

class TarjetaPropiedad(Base):
    numero_tarjeta = Column(BigInteger, primary_key=True, index=True)
    nombre_propietario = Column(String(250), nullable=False)
    cilindraje = Column(Integer, nullable=False)
    documento_propietario = Column(BigInteger, nullable=False)
    marca = Column(String(150), nullable=False)
    clase_vehiculo = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)
    servicio = Column(String(100), nullable=False)
    tipo_carroceria = Column(String(100), nullable=False)
    linea_vehiculo = Column(String(100), nullable=False)
    numero_motor = Column(BigInteger, nullable=False)
    combustible = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    placa = Column(String(6), nullable=False)
    
    #foraneas
    fk_placavehiculo = Column(String(6), ForeignKey('vehiculo.placa'), nullable=False)
    
    