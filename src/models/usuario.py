from sqlalchemy import Column, BigInteger, String, Date
from src.db.base_class import Base
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = "usuarios"
    documento_identidad = Column(BigInteger, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_registro = Column(Date, nullable=False, default=func.now())
    correo = Column(String(100), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    rol = Column(String(100), nullable=False)

