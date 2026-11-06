
"""Operaciones para registrar y modificar clientes."""

import sqlite3
from pathlib import Path

from validaciones.validaciones import (
    validar_id_positivo,
    validar_telefono_celular,
    validar_texto_requerido,
)
from datos.database import DATABASE_PATH, conectar_db


def registrar_cliente(
    nombre: str,
    correo: str,
    telefono_celular: str,
    ruta_db: Path = DATABASE_PATH,
) -> int:
    """Guardar un cliente y devolver el identificador que asigno SQLite."""
    nombre = validar_texto_requerido(nombre, "El nombre")
    correo = validar_texto_requerido(correo, "El correo")
    telefono_celular = validar_telefono_celular(telefono_celular)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                INSERT INTO clientes (nombre, correo, telefono)
                VALUES (?, ?, ?)
                """,
                (nombre, correo, telefono_celular),
            )
            return cursor.lastrowid
    finally:
        conexion.close()


def modificar_cliente(
    cliente_id: int,
    nombre: str,
    correo: str,
    telefono: str,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Actualizar un cliente existente o indicar que su ID no existe."""
    cliente_id = validar_id_positivo(cliente_id, "cliente")
    nombre = validar_texto_requerido(nombre, "El nombre")
    correo = validar_texto_requerido(correo, "El correo")
    telefono = validar_telefono_celular(telefono)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                UPDATE clientes
                SET nombre = ?, correo = ?, telefono = ?
                WHERE id = ?
                """,
                (nombre, correo, telefono, cliente_id),
            )
            if cursor.rowcount == 0:
                raise LookupError(f"No existe un cliente con ID {cliente_id}")
    finally:
        conexion.close()