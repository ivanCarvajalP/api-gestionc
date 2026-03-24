from sqlalchemy import Column, Double, String, Date, ForeignKey
from src.db.base_class import Base

class Factura(Base):
    #la longitud de un codigo CUFE es de 64 caracteres
    id_factura = Column(String(80), primary_key=True, index=True)
    fecha_factura = Column(Date, nullable=False)
    nombre_empresa = Column(String(200), nullable=False)
    costo_total = Column(Double, nullable=False)
    url_factura = Column(String(250), nullable=True)

    #foraneas
    fk_placavehiculo = Column(String(6), ForeignKey('vehiculo.placa'), nullable=False)
    
