from sqlalchemy import Column, Integer, String
from src.db.base_class import Base

class Vehiculo(Base):
    placa = Column(String(6), primary_key=True, index=True)
    cilindraje = Column(Integer, nullable=False)
    marca = Column(String(100), nullable=False)