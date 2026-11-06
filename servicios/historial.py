
"""Consultas del historial de servicios de un cliente."""

import sqlite3
from pathlib import Path
from typing import List

from validaciones.validaciones import validar_id_positivo
from datos.database import DATABASE_PATH, conectar_db


def consultar_historial_cliente(
    cliente_id: int,
    ruta_db: Path = DATABASE_PATH,
) -> List[sqlite3.Row]:
    """Devolver los servicios del cliente, del mas reciente al mas antiguo."""
    cliente_id = validar_id_positivo(cliente_id, "cliente")
    conexion = conectar_db(ruta_db)
    conexion.row_factory = sqlite3.Row

    try:
        cursor = conexion.execute(
            """
            SELECT id, cliente_id, vehiculo, descripcion, producto, valor, fecha
            FROM servicios
            WHERE cliente_id = ?
            ORDER BY fecha DESC, id DESC
            """,
            (cliente_id,),
        )
        return cursor.fetchall()
    finally:
        conexion.close()