from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioCreate, UsuarioUpdate

def obtener_usuarios(db: Session):
    query = text("SELECT * FROM usuarios")
    resultados = db.execute(query).mappings().all()
    return [dict(row) for row in resultados]


def obtener_usuario_por_documento(documento_identidad: int, db: Session):
    query = text("SELECT * FROM usuarios WHERE documento_identidad = :doc_id")
    resultado = db.execute(query, {"doc_id": documento_identidad}).mappings().first()
    return dict(resultado) if resultado else None

def obtener_usuario_por_correo(correo: str, db: Session):
    query = text("SELECT * FROM usuarios WHERE correo = :correo_usuario LIMIT 1")
    resultado = db.execute(query, {"correo_usuario": correo}).mappings().first()
    return dict(resultado) if resultado else None


def crear_usuario(db: Session, usuario: UsuarioCreate):
    query = text(
        """INSERT INTO usuarios 
        (documento_identidad, nombres, apellidos, correo, fecha_nacimiento, rol, fecha_registro) 
        VALUES (:documento_identidad, :nombres, :apellidos, :correo, :fecha_nacimiento, 'usuario', CURRENT_DATE)
        RETURNING *
        """)
    
    resultado = db.execute(query, {
        "documento_identidad": usuario.documento_identidad, 
        "nombres": usuario.nombres, 
        "apellidos": usuario.apellidos, 
        "correo": usuario.correo, 
        "fecha_nacimiento": usuario.fecha_nacimiento
        }).mappings().first()
        
    db.commit()
    
    # Devolvemos el diccionario con todos los datos que PostgreSQL insertó
    return dict(resultado)

def actualizar_usuario(documento_identidad: int, usuario: UsuarioUpdate, db: Session):
    query = text(
        """UPDATE usuarios 
        SET nombres = :nombres, apellidos = :apellidos, correo = :correo, fecha_nacimiento = :fecha_nacimiento
        WHERE documento_identidad = :documento_identidad
        RETURNING *""")
    
    resultado = db.execute(query, {
        "documento_identidad": documento_identidad,
        "nombres": usuario.nombres,
        "apellidos": usuario.apellidos,
        "correo": usuario.correo,
        "fecha_nacimiento": usuario.fecha_nacimiento
        }).mappings().first()
    
    db.commit()
    return dict(resultado) if resultado else None


def obtener_vehiculos_de_un_usuario(documento_identidad: int, db: Session):
    query = text("SELECT * FROM vehiculos WHERE documento_identidad = :doc_id")
    resultado = db.execute(query, {"doc_id": documento_identidad}).mappings().all()
    return [dict(row) for row in resultado]
    