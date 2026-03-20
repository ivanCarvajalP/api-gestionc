from sqlalchemy import Column, BigInteger, String, Date
from src.db.base_class import Base

class Usuario(Base):
    documento_identidad = Column(BigInteger, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    rol = Column(String(100), nullable=False)

