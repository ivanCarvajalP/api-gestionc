"""alter tables nombre de las tablas

Revision ID: 9dae10319778
Revises: 0ac767af2573
Create Date: 2026-03-24 16:38:45.084581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dae10319778'
down_revision: Union[str, Sequence[str], None] = '0ac767af2573'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alembic intenta hacer DROP a las tablas viejas y CREATE a las nuevas
    # lo cual falla porque otras tablas dependen de ellas (Foreign Keys).
    # La solución correcta en SQL es usar RENAME_TABLE.
    op.rename_table('usuario', 'usuarios')
    op.rename_table('vehiculo', 'vehiculos')
    op.rename_table('factura', 'facturas')
    op.rename_table('servicio', 'servicios')
    
    # Renombrar los índices para que sigan coincidiendo con el modelo autogenerado
    op.execute('ALTER INDEX ix_usuario_documento_identidad RENAME TO ix_usuarios_documento_identidad')
    op.execute('ALTER INDEX ix_vehiculo_placa RENAME TO ix_vehiculos_placa')
    op.execute('ALTER INDEX ix_factura_id_factura RENAME TO ix_facturas_id_factura')
    op.execute('ALTER INDEX ix_servicio_id_servicio RENAME TO ix_servicios_id_servicio')


def downgrade() -> None:
    # Proceso inverso si necesitas regresar a la versión anterior
    op.rename_table('usuarios', 'usuario')
    op.rename_table('vehiculos', 'vehiculo')
    op.rename_table('facturas', 'factura')
    op.rename_table('servicios', 'servicio')

    op.execute('ALTER INDEX ix_usuarios_documento_identidad RENAME TO ix_usuario_documento_identidad')
    op.execute('ALTER INDEX ix_vehiculos_placa RENAME TO ix_vehiculo_placa')
    op.execute('ALTER INDEX ix_facturas_id_factura RENAME TO ix_factura_id_factura')
    op.execute('ALTER INDEX ix_servicios_id_servicio RENAME TO ix_servicio_id_servicio')
