"""Consultas de busqueda de clientes."""

import sqlite3
from pathlib import Path
from typing import List

from validaciones.validaciones import validar_texto_requerido
from datos.database import DATABASE_PATH, conectar_db


def listar_clientes(ruta_db: Path = DATABASE_PATH) -> List[sqlite3.Row]:
    """Devolver todos los clientes ordenados por nombre."""
    conexion = conectar_db(ruta_db)
    conexion.row_factory = sqlite3.Row

    try:
        cursor = conexion.execute(
            """
            SELECT id, nombre, correo, telefono
            FROM clientes
            ORDER BY nombre COLLATE NOCASE, id
            """
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def buscar_clientes(
    termino: str,
    ruta_db: Path = DATABASE_PATH,
) -> List[sqlite3.Row]:
    """Buscar por coincidencias parciales en el nombre o el telefono."""
    termino = validar_texto_requerido(termino, "La busqueda")
    conexion = conectar_db(ruta_db)
    conexion.row_factory = sqlite3.Row

    try:
        cursor = conexion.execute(
            """
            SELECT id, nombre, correo, telefono
            FROM clientes
            WHERE nombre LIKE ? OR telefono LIKE ?
            ORDER BY nombre COLLATE NOCASE, id
            """,
            (f"%{termino}%", f"%{termino}%"),
        )
        return cursor.fetchall()
    finally:
        conexion.close()