from sqlalchemy import Column, Integer, String, Double, ForeignKey
from src.db.base_class import Base

class Servicio(Base):
    __tablename__ = "servicios"
    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(Double, nullable=False)
    cantidad = Column(Integer, nullable=False)

    #foraneas
    fk_idfactura = Column(String(80), ForeignKey('facturas.id_factura'), nullable=False)
    